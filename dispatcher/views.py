import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from orders.models import Order
from dispatcher.models import DispatchTask
from drivers.models import Driver
from trips.models import Trip
from vehicles.models import Vehicle
from users.models import Profile
from routes.models import Route
from .utils import get_optimal_vehicle_only
from django.utils.timezone import now
from datetime import timedelta

@csrf_protect
@require_http_methods(["POST"])
def assign_order_dispatch(request):
    try:
        data = json.loads(request.body)
        order_id = data.get("order_id")
        dispatcher_id = data.get("dispatcher_id")
        driver_id = data.get("driver_id")

        order = get_object_or_404(Order, id=order_id)
        if order.status != 'pending':
            return JsonResponse({"error": "Order already processed"}, status=400)

        # Dispatcher validation
        dispatcher = Profile.objects.filter(id=dispatcher_id, role="dispatcher").first()
        if not dispatcher:
            return JsonResponse({"error": "Dispatcher not found or invalid"}, status=400)

        # Driver validation
        driver = Driver.objects.get(id=driver_id, availability=True)
        if Trip.objects.filter(driver=driver, end_time__isnull=True).exists():
            return JsonResponse({"error": "Driver already has an active trip"}, status=400)

        driver_profile = Profile.objects.get(user=driver.user, role="driver")

        # Get optimal vehicle
        optimal_vehicle = get_optimal_vehicle_only()
        if not optimal_vehicle:
            return JsonResponse({"error": "No available vehicle found"}, status=400)

        # Create a new trip
        trip = Trip.objects.create(
            route=order.route,
            vehicle=optimal_vehicle,
            driver=driver,
            start_time=now(),
            end_time=None,
            status='scheduled'
        )

        # Create dispatch task
        DispatchTask.objects.create(
            dispatcher=dispatcher,
            driver=driver_profile,
            vehicle=optimal_vehicle,
            route=order.route,
            trip=trip
        )

        # Update statuses
        driver.availability = False
        driver.save()

        optimal_vehicle.status = 'inactive'
        optimal_vehicle.save()

        order.status = 'assigned'
        order.save()

        return JsonResponse({
            "message": "Trip created and order assigned.",
            "order_id": order.id,
            "trip_id": trip.id,
            "vehicle_id": optimal_vehicle.id,
            "driver_id": driver_profile.id,
            "dispatcher_id": dispatcher.id
        }, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
