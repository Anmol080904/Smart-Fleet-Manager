import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from .models import Vehicle

# Utility to check dispatcher access
def is_dispatcher(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'dispatcher'

@csrf_protect
@require_http_methods(["POST"])
def register_vehicle(request):
    if not is_dispatcher(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        data = json.loads(request.body)

        license_plate = data['license_plate']
        model = data['model']
        capacity = data['capacity']
        fuel_type = data['fuel_type']
        status = data.get('status', 'active')

        if Vehicle.objects.filter(license_plate=license_plate).exists():
            return JsonResponse({'error': 'Vehicle with this license plate already exists'}, status=400)

        vehicle = Vehicle.objects.create(
            license_plate=license_plate,
            model=model,
            capacity=capacity,
            fuel_type=fuel_type,
            status=status
        )

        return JsonResponse({'message': 'Vehicle registered successfully', 'vehicle_id': vehicle.id}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def list_vehicles(request):
    if not is_dispatcher(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    vehicles = Vehicle.objects.all()
    data = [{
        'id': v.id,
        'license_plate': v.license_plate,
        'model': v.model,
        'capacity': v.capacity,
        'fuel_type': v.fuel_type,
        'status': v.status,
        'registration_date': v.registration_date.strftime("%Y-%m-%d")
    } for v in vehicles]

    return JsonResponse(data, safe=False)


@csrf_protect
@require_http_methods(["POST"])
def update_vehicle(request, vehicle_id):
    if not is_dispatcher(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        data = json.loads(request.body)

        vehicle.model = data.get('model', vehicle.model)
        vehicle.capacity = data.get('capacity', vehicle.capacity)
        vehicle.fuel_type = data.get('fuel_type', vehicle.fuel_type)
        vehicle.status = data.get('status', vehicle.status)
        vehicle.save()

        return JsonResponse({'message': 'Vehicle updated successfully'})

    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_protect
@require_http_methods(["POST"])
def delete_vehicle(request, vehicle_id):
    if not is_dispatcher(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        vehicle.delete()
        return JsonResponse({'message': 'Vehicle deleted successfully'})
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
