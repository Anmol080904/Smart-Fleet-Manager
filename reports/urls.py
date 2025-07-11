from django.urls import path
from .views import download_fuel_report, download_maintenance_report

urlpatterns = [
    path('fuel/', download_fuel_report),
    path('maintenance/', download_maintenance_report),
]
