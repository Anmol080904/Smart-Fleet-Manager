import pandas as pd
from django.http import HttpResponse
from fuel.models import FuelLog
from maintanence.models import MaintenanceLog
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def download_fuel_report(request):
    logs = FuelLog.objects.select_related("vehicle")
    df = pd.DataFrame([{
        "Vehicle": log.vehicle.license_plate,
        "Quantity": log.quantity,
        "Cost": log.cost,
        "Date": log.date.strftime("%Y-%m-%d")
    } for log in logs])
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="fuel_logs.xlsx"'
    df.to_excel(response, index=False)
    return response

@require_http_methods(["GET"])
def download_maintenance_report(request):
    logs = MaintenanceLog.objects.select_related("vehicle")
    df = pd.DataFrame([{
        "Vehicle": log.vehicle.license_plate,
        "Type": log.type,
        "Date": log.date.strftime("%Y-%m-%d"),
        "Description": log.description,
        "Cost": log.cost
    } for log in logs])
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="maintenance_logs.xlsx"'
    df.to_excel(response, index=False)
    return response
