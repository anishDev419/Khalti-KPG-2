import base64
import hashlib

from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from decouple import config

from django.utils import timezone
from connectips.forms import ConnectForm


class Index(TemplateView):
    # INITIAL PAYMENT PAGE TEMPLATE
    template_name = 'payment/connectips/index.html'

    def dispatch(self, *args, **kwargs):
        # REQUIRED EXTRA BUSINESS LOGIC
        print("INDEX CONNECTIPS")
        return super().dispatch(*args, **kwargs)


class Submit(FormView):
    template_name = 'payment/connectips/index.html'
    form_class = ConnectForm
    success_url = '/connectips/form-redirect/'

    def form_valid(self, form):

        try:
            # ACCESS FORM DATA
            txn_crncy = form.cleaned_data['TXNCRNCY']
            txn_amt = form.cleaned_data['TXNAMT']
            remarks = form.cleaned_data['REMARKS']

            # PERFORM REQUIRED BUSINESS LOGIC

            # AMOUNT: RUPEES TO PAISA
            txn_amt = txn_amt * 100
            merchant_id = config('connect_merchant_id')
            app_id = config('connect_app_id')
            app_name = config('connect_app_name')
            url = config('connect_url')

            # FIX KEY FORMAT
            env_key = config('CONNECT_PRIVATE_KEY')
            format_key = env_key.replace('\\n', '\n')

            # GENERATE TXN ID
            current_time = timezone.now()
            timestamp_str = current_time.strftime("%Y%m%d%H%M%S%f")
            txn_id = f'{timestamp_str}_{app_id}'

            txn_date = current_time.strftime("%d-%m-%Y")

            # Prepare data for POST request
            data = {
                'MERCHANTID': merchant_id,
                'APPID': app_id,
                'APPNAME': app_name,
                'TXNID': txn_id,
                'TXNDATE': txn_date,
                'TXNCRNCY': txn_crncy,
                'TXNAMT': txn_amt,
                'REFERENCEID': txn_id,
                'REMARKS': remarks,
                'PARTICULARS': remarks,
                'TOKEN': 'TOKEN'
            }

            print('data without token: ', data)

            # FORMAT PLAINTEXT DATA
            plaintext_data = ", ".join([f"{key}={value}" for key, value in data.items()]) + ", TOKEN=TOKEN"

            # Hash the message using SHA256
            hash_object = hashlib.sha256()
            hash_object.update(plaintext_data.encode())
            hash_object.update(format_key.encode())
            hashed_message = hash_object.hexdigest()

            # base64 FORMATTING AND APPENDING TO DATA
            decoded_bytes = bytes.fromhex(hashed_message)
            encoded_base64 = base64.b64encode(decoded_bytes).decode()
            data['TOKEN'] = encoded_base64

            print('form post data', data)

            # FORM POST
            return render(self.request, 'payment/connectips/form_post.html', {'form_data': data})

        except Exception as e:
            print(e)
            return super().form_invalid(form)


class FormRedirect(TemplateView):
    template_name = 'payment/connectips/form_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.request.GET  # Access query parameters
        print('TEMPALTE VIEW DATA', context['data'])
        return context


class SuccessForm(TemplateView):
    template_name = 'payment/connectips/success.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['message'] = 'Hello World!'
        return context
