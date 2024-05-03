from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def Return_URL(request):
    if request.method == 'GET':
        pidx = request.GET.get('pidx')
        transaction_id = request.GET.get('transaction_id')
        status = request.GET.get('status')

        if status and status == "Completed" and pidx and transaction_id:
            # DATA HANDLING VERIFICATION OF TRANSACTION
            print("Completed")
            return render(request, 'payment/khalti/success.html')
        else:
            return render(request, 'payment/khalti/failed.html')
            pass


    else:
        # Return an error response for other HTTP methods
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
