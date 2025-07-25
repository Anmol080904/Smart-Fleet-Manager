import json
import requests
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from vehicles.models import Vehicle
from .models import Driver
from users.models import Profile

# ---- Helper ----
def is_dispatcher(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'dispatcher'

# ---- Create Driver ----
@csrf_protect
@require_http_methods(["POST"])
def create_driver(request):
    if not is_dispatcher(request.user):
        return JsonResponse({'error': 'Unauthorized: Only dispatchers allowed'}, status=401)
    try:
        data = json.loads(request.body)

        username = data["username"]
        email = data["email"]
        password = data["password"]
        license_number = data["license_number"]
        license_expiry_date = data.get("license_expiry_date")
        vehicle_id = data.get("vehicle_id")
        phone_number = data["phone_number"]
        address = data["address"]
        date_of_birth = data["date_of_birth"]
        experience_years = data["experience_years"]
        emergency_contact = data["emergency_contact"]

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, role="driver")
        vehicle = Vehicle.objects.get(id=vehicle_id) if vehicle_id else None

        driver = Driver.objects.create(
            user=user,
            license_number=license_number,
            license_expiry_date=license_expiry_date,
            assigned_vehicle=vehicle,
            availability=True,
            phone_number=phone_number,
            address=address,
            date_of_birth=date_of_birth,
            experience_years=experience_years,
            emergency_contact=emergency_contact
        )

        return JsonResponse({'message': 'Driver created successfully', 'driver_id': driver.id}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ---- List Drivers ----
@csrf_protect
@require_http_methods(["GET"])
def list_drivers(request):
    if not is_dispatcher(request.user):
        return JsonResponse({'error': 'Unauthorized: Only dispatchers allowed'}, status=401)

    drivers = Driver.objects.select_related('user', 'assigned_vehicle').all()
    data = [{
        'id': d.id,
        'username': d.user.username,
        'email': d.user.email,
        'license_number': d.license_number,
        'availability': d.availability,
        'vehicle': {
            'id': d.assigned_vehicle.id,
            'license_plate': d.assigned_vehicle.license_plate
        } if d.assigned_vehicle else None
    } for d in drivers]

    return JsonResponse(data, safe=False)

# ---- Update Driver ----
@csrf_protect
@require_http_methods(["POST"])
def update_driver(request, driver_id):
    if not is_dispatcher(request.user):
        return JsonResponse({'error': 'Unauthorized: Only dispatchers allowed'}, status=401)

    try:
        driver = Driver.objects.select_related('user').get(id=driver_id)
        data = json.loads(request.body)

        driver.license_number = data.get('license_number', driver.license_number)
        driver.availability = data.get('availability', driver.availability)
        vehicle_id = data.get('vehicle_id')

        if vehicle_id:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            driver.assigned_vehicle = vehicle

        driver.save()
        return JsonResponse({'message': 'Driver updated successfully'})

    except Driver.DoesNotExist:
        return JsonResponse({'error': 'Driver not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ---- Delete Driver ----
@csrf_protect
@require_http_methods(["POST"])
def delete_driver(request, driver_id):
    if not is_dispatcher(request.user):
        return JsonResponse({'error': 'Unauthorized: Only dispatchers allowed'}, status=401)

    try:
        driver = Driver.objects.select_related('user').get(id=driver_id)
        user = driver.user
        driver.delete()
        user.delete()
        return JsonResponse({'message': 'Driver and user deleted successfully'})
    except Driver.DoesNotExist:
        return JsonResponse({'error': 'Driver not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ---- Toggle Driver Availability ----
@csrf_protect
@require_http_methods(["POST"])
def toggle_availability(request):
    user = request.user

    if not user.is_authenticated or not hasattr(user, 'profile') or user.profile.role != 'driver':
        return JsonResponse({'error': 'Unauthorized: Only drivers allowed'}, status=401)

    try:
        driver = Driver.objects.get(user=user)
        data = json.loads(request.body)
        new_status = data.get("availability")

        if new_status is None:
            return JsonResponse({'error': 'Missing "availability" in request body'}, status=400)

        driver.availability = bool(new_status)
        driver.save()

        return JsonResponse({'message': 'Availability updated', 'availability': driver.availability}, status=200)

    except Driver.DoesNotExist:
        return JsonResponse({'error': 'Driver profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


AI_MICROSERVICE_URL = "http://localhost:5001"  

@csrf_protect
@require_http_methods(["POST"])
def start_trip(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or request.user.profile.role != 'driver':
        return JsonResponse({'error': 'Unauthorized: Only drivers can start trip'}, status=401)

    try:
        res = requests.post(f"{AI_MICROSERVICE_URL}/start-monitor")
        if res.status_code == 200:
            return JsonResponse({'message': 'Trip started, monitoring enabled'})
        else:
            return JsonResponse({'error': 'Failed to start monitoring'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Error contacting AI microservice: {str(e)}'}, status=500)

@csrf_protect
@require_http_methods(["POST"])
def pause_trip(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or request.user.profile.role != 'driver':
        return JsonResponse({'error': 'Unauthorized: Only drivers can pause trip'}, status=401)

    try:
        res = requests.post(f"{AI_MICROSERVICE_URL}/stop-monitor")
        if res.status_code == 200:
            return JsonResponse({'message': 'Trip paused, monitoring stopped'})
        else:
            return JsonResponse({'error': 'Failed to stop monitoring'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Error contacting AI microservice: {str(e)}'}, status=500)

@csrf_protect
@require_http_methods(["POST"])
def end_trip(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'profile') or request.user.profile.role != 'driver':
        return JsonResponse({'error': 'Unauthorized: Only drivers can end trip'}, status=401)

    try:
        res = requests.get(f"{AI_MICROSERVICE_URL}/check-drowsy")
        if res.status_code == 200:
            result = res.json()
            return JsonResponse({'message': 'Trip ended', 'drowsy': result.get("drowsy")})
        else:
            return JsonResponse({'error': 'Failed to get drowsiness status'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Error contacting AI microservice: {str(e)}'}, status=500)
