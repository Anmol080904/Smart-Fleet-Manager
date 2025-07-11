from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from .models import FuelLog
import json

@csrf_protect
@require_http_methods(["POST"])
def create_fuel_log(request):
    try:
        data = json.loads(request.body)
        log = FuelLog.objects.create(
            vehicle_id=data['vehicle_id'],
            date=data['date'],
            quantity=data['quantity'],
            cost=data['cost'],
        )
        return JsonResponse({'message': 'Fuel log created successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def list_fuel_logs(request):
    logs = FuelLog.objects.all().select_related('vehicle')
    data = [{
        'id': log.id,
        'vehicle': log.vehicle.license_plate,
        'date': log.date,
        'quantity': log.quantity,
        'cost': log.cost,
    } for log in logs]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_http_methods(["DELETE"])
def delete_fuel_log(request, log_id):
    try:
        FuelLog.objects.get(id=log_id).delete()
        return JsonResponse({'message': 'Fuel log deleted successfully'})
    except FuelLog.DoesNotExist:
        return JsonResponse({'error': 'Log not found'}, status=404)