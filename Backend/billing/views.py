# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.http import require_http_methods
import paypalrestsdk
from django.conf import settings

import os
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": os.environ.get("PAYPAL_CLIENT_ID"),
    "client_secret": os.environ.get("PAYPAL_CLIENT_SECRET")
})

from orders.models import Order
from billing.models import Payment  # Your payment model

@csrf_exempt
@require_http_methods(["POST"])
def initiate_payment(request):
    try:
        data = json.loads(request.body)
        amount = data.get("amount")
        order_id = data.get("order_id")

        if not amount or not order_id:
            return JsonResponse({"error": "amount and order_id required"}, status=400)

        # Check if order exists
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/success",  
                "cancel_url": "http://localhost:8000/payment/cancel"
            },
            "transactions": [{
                "amount": {
                    "total": f"{float(amount):.2f}",
                    "currency": "USD"
                },
                "description": f"Payment for Order #{order_id}"
            }]
        })

        if payment.create():
            # Save payment to DB as pending
            Payment.objects.create(
                order=order,
                payment_id=payment.id,
                amount=amount,
                status="pending",
                currency="USD"
            )

            # Find PayPal approval URL
            for link in payment.links:
                if link.rel == "approval_url":
                    return JsonResponse({
                        "message": "Payment created successfully",
                        "paypal_url": link.href,
                        "payment_id": payment.id
                    })
            return JsonResponse({"error": "No approval URL returned"}, status=500)
        else:
            return JsonResponse({"error": payment.error}, status=500)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@csrf_exempt
@require_http_methods(["GET"])
def payment_success(request):
    payment_id = request.GET.get("payment_id")
    if not payment_id:
        return JsonResponse({"error": "Missing payment_id"}, status=400)

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.state == "approved":
        # Update DB
        Payment.objects.filter(payment_id=payment_id).update(status="completed")
        return JsonResponse({"message": "Payment completed successfully!"})
    else:
        return JsonResponse({"error": "Payment not approved"}, status=400)
@csrf_exempt
@require_http_methods(["GET"])
def payment_cancel(request):
    payment_id = request.GET.get("payment_id")
    if payment_id:
        Payment.objects.filter(payment_id=payment_id).update(status="failed")
    return JsonResponse({"message": "Payment was cancelled."})
