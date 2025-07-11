from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from .models import MaintenanceLog
import json

@csrf_protect
@require_http_methods(["POST"])
def create_maintenance(request):
    try:
        data = json.loads(request.body)
        log = MaintenanceLog.objects.create(
            vehicle_id=data['vehicle_id'],
            type=data['type'],
            date=data['date'],
            description=data.get('description', ''),
            cost=data['cost'],
            km_at_service=data.get('km_at_service')
        )
        return JsonResponse({'message': 'Maintenance log created successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def list_maintenance(request):
    logs = MaintenanceLog.objects.all().select_related('vehicle')
    data = [{
        'id': log.id,
        'vehicle': log.vehicle.license_plate,
        'type': log.type,
        'date': log.date,
        'description': log.description,
        'cost': log.cost,
        'km_at_service': log.km_at_service
    } for log in logs]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_http_methods(["DELETE"])
def delete_maintenance(request, log_id):
    try:
        MaintenanceLog.objects.get(id=log_id).delete()
        return JsonResponse({'message': 'Maintenance log deleted successfully'})
    except MaintenanceLog.DoesNotExist:
        return JsonResponse({'error': 'Log not found'}, status=404)
