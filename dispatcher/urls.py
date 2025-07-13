from django.urls import path
from .views import (
    assign_order_dispatch
)

urlpatterns = [
    path('assign/', assign_order_dispatch, name='create-dispatch'),
   
]
