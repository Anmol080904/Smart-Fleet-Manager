from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_fuel_log, name='create-fuel'),
    path('list/', views.list_fuel_logs, name='list-fuel'),
    path('delete/<int:log_id>/', views.delete_fuel_log, name='delete-fuel'),
]
