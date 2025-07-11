from django.urls import path
from .views import initiate_payment, payment_success, payment_cancel

urlpatterns = [
    path('payment/initiate/', initiate_payment),
    path('payment/success', payment_success),
    path('payment/cancel', payment_cancel),
]
