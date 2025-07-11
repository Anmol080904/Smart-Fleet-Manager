from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Trip
from routes.models import Route
from vehicles.models import Vehicle
from drivers.models import Driver
from django.utils.dateparse import parse_datetime
import json

@csrf_exempt
@require_http_methods(["POST"])
def create_trip(request):
    try:
        data = json.loads(request.body)

        # Log incoming data (optional, for debugging)
        print("Incoming Trip Data:", data)

        # Validate existence
        route = Route.objects.get(id=data['route_id'])
        vehicle = Vehicle.objects.get(id=data['vehicle_id'])
        driver = Driver.objects.get(id=data['driver_id'])

        # Parse times
        start_time = parse_datetime(data['start_time'])
        end_time = parse_datetime(data.get('end_time')) if data.get('end_time') else None

        # Create trip
        trip = Trip.objects.create(
            route=route,
            vehicle=vehicle,
            driver=driver,
            start_time=start_time,
            end_time=end_time,
            status=data.get('status', 'scheduled')
        )

        return JsonResponse({
            "message": "Trip created successfully",
            "trip_id": trip.id,
            "driver": driver.user.username,
            "vehicle_id": vehicle.id
        }, status=201)

    except Route.DoesNotExist:
        return JsonResponse({'error': 'Invalid route_id'}, status=400)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Invalid vehicle_id'}, status=400)
    except Driver.DoesNotExist:
        return JsonResponse({'error': 'Invalid driver_id'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
