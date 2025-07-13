from django.urls import path
from customers.views import (
    create_order,
    cancel_order_by_customer,
    check_order_status,
    register_customer,
    login_customer,
    logout_customer
)

urlpatterns = [
    path('create/',register_customer),
    path('login/',login_customer),
    path('logout/',logout_customer),
    path('create-order/', create_order),
    path('cancel-order/', cancel_order_by_customer),
    path('status-order/', check_order_status),
]
