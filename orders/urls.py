from django.urls import path
from .views import create_order #list_orders

urlpatterns = [
    path('create/', create_order),
    # path('list/', list_orders),
]
