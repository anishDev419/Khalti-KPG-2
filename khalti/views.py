from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView

from khalti.forms import InitiateForm

from django.http import HttpResponseRedirect

import json
import requests
import re
from django.utils import timezone
import uuid

from decouple import config


# Create your views here.

class Index(TemplateView):
    template_name = 'payment/khalti/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['message'] = 'Hello World!'
        return context


class Submit(FormView):
    template_name = 'payment/khalti/index.html'
    form_class = InitiateForm
    success_url = '/khalti/success-form-khalti/'

    def form_valid(self, form):

        try:
            # GENERATING KHALTI'S PAYLOAD

            # GET REQUEST URL
            url = config('khalti_url') + "epayment/initiate/"

            # GET IMAGIO CREATIONS WEBSITE URL
            website_url = config('imagio_website_url')

            # GENERATE RETURN URL
            main_domain = config('MAIN_DOMAIN')

            if re.search(r'http://', main_domain):
                return_url = main_domain + "/khalti/return-khalti/"
            else:
                return_url = "http://" + main_domain + "/khalti/return-khalti"

            # AMOUNT PAYLOAD
            amount_in_r = self.request.POST.get('amount')
            amount = int(amount_in_r) * 100

            # TEMPORARILY GENERATE PURCHASE INFO (DB | SUBSCRIPTION)
            current_time = timezone.now()
            timestamp_str = current_time.strftime("%Y%m%d%H%M%S%f")
            purchase_order_name = "instance_" + timestamp_str
            purchase_order_id = "instance_renew_id_" + timestamp_str

            auth_key = "Key " + config('khalti_key')
            payload = {
                "return_url": return_url,
            # GENERATE SECRET KEY FORMAT
                "website_url": website_url,
                "amount": amount,
                "purchase_order_id": purchase_order_id,
                "purchase_order_name": purchase_order_name,
                "customer_info": {
                    "name": "Instance Name",
                    "email": "instance@imagio-creations.com",
                    "phone": "9803067188"
                }
            }
            headers = {
                'Authorization': auth_key,
                'Content-Type': 'application/json',
            }

            response = requests.post(url, headers=headers, json=payload)
            res_json = response.json()

            if response.status_code == 200:
                if 'pidx' in res_json and 'payment_url' in res_json:
                    pidx = res_json.get('pidx')
                    payment_url = res_json.get('payment_url')
                    if pidx in payment_url:
                        # GOOD CASE BEFORE REDIRECTING
                        return HttpResponseRedirect(payment_url)

                    else:
                        # INSERT INVOICE ERROR CODE
                        # HANDLE BAD CASE
                        # HANDLING ERROR MESSAGE
                        print("Error: ", response)
                        return super().form_invalid(form)

                elif 'error_key' in res_json:
                    # INSERT INVOICE ERROR CODE
                    # HANDLE BAD CASE
                    # HANDLING ERROR MESSAGE
                    print("Error: ", response)
                    return super().form_invalid(form)

                else:
                    # INSERT INVOICE ERROR CODE
                    # HANDLE BAD CASE
                    print("Error: ", response)
                    return super().form_invalid(form)
            else:
                # INSERT INVOICE ERROR CODE
                # HANDLE BAD CASE
                return super().form_invalid(form)

        except Exception as e:
            # INSERT INVOICE ERROR CODE
            # HANDLE BAD CASE
            return super().form_invalid(form)

    def form_invalid(self, form):
        # HANDLE BAD CASE
        # HANDLING ERROR MESSAGE
        print("Form errors:", form.errors)
        return super().form_invalid(form)


@csrf_exempt
def ReturnURL(request):
    if request.method == 'GET':
        pidx = request.GET.get('pidx')
        transaction_id = request.GET.get('transaction_id')
        status = request.GET.get('status')

        if status and status == "Completed" and pidx and transaction_id:
            # DATA HANDLING VERIFICATION OF TRANSACTION

            # GENERATING URL
            url = config('khalti_url') + "epayment/lookup/"
            print("url: ", url)

            # GENERATE SECRET KEY FORMAT
            auth_key = "Key " + config('khalti_key')
            payload = {
                "pidx": pidx,
            }
            headers = {
                'Authorization': auth_key,
                'Content-Type': 'application/json',
            }

            response = requests.post(url, headers=headers, json=payload)
            res_json = response.json()

            if response.status_code == 200:

                if 'pidx' in res_json and 'status' in res_json:
                    pidx = res_json.get('pidx')
                    status = res_json.get('status')
                    if pidx and status and status == "Completed":
                        # HANDLE GOOD CASE
                        print("res_json: ", res_json)
                        return render(request, 'payment/khalti/success.html')

                    else:
                        # INSERT INVOICE ERROR CODE
                        # HANDLE BAD CASE
                        # HANDLING ERROR MESSAGE
                        print("Error: ", response)
                        return render(request, 'payment/khalti/failed.html')

                elif 'error_key' in res_json:
                    # INSERT INVOICE ERROR CODE
                    # HANDLE BAD CASE
                    # HANDLING ERROR MESSAGE
                    print("Error: ", response)
                    return render(request, 'payment/khalti/failed.html')

                else:
                    # INSERT INVOICE ERROR CODE
                    # HANDLE BAD CASE
                    print("Error: ", response)
                    return render(request, 'payment/khalti/failed.html')
            else:

                # INSERT INVOICE ERROR CODE
                # HANDLE BAD CASE
                return render(request, 'payment/khalti/failed.html')

        else:

            # INSERT INVOICE ERROR CODE
            # HANDLE BAD CASE
            return render(request, 'payment/khalti/failed.html')


class SuccessForm(TemplateView):
    template_name = 'payment/khalti/success.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['message'] = 'Hello World!'
        return context
