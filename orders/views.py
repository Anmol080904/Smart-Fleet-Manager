import os
import json
from datetime import timedelta
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Order
from dispatcher.models import DispatchTask
from drivers.models import Driver
from trips.models import Trip
from users.models import Profile
from django.contrib.auth.models import User
from vehicles.models import Vehicle
from routes.models import Route
from routes.utils import fetch_route_from_ors, haversine_distance
from orders.utils import get_optimal_vehicle_only 
from django.shortcuts import get_object_or_404
@csrf_protect
@require_http_methods(["POST"])
def create_order(request):
    try:
        data = json.loads(request.body)
        customer = data['customer_name']
        origin = data['origin']
        destination = data['destination']
        load_weight = data['load_weight']
        deadline = data['deadline']
        dispatcher_id = data['dispatcher_id']
        driver_id = data['driver_id']
        trip_id = data['trip_id']  # provided externally
        status = data.get('status', 'pending')

        # Parse coordinates
        start_coords = tuple(map(float, origin.split(',')))
        end_coords = tuple(map(float, destination.split(',')))

        # Route calculation
        api_key = os.environ.get("ORS_API_KEY")
        waypoints, distance, duration = fetch_route_from_ors(start_coords, end_coords, api_key)

        if not waypoints or not isinstance(distance, (int, float)):
            distance = haversine_distance(*start_coords, *end_coords)
            duration = timedelta(hours=distance / 40)
            waypoints = [
                {"lat": start_coords[0], "lng": start_coords[1]},
                {"lat": end_coords[0], "lng": end_coords[1]}
            ]

        # Create route
        route = Route.objects.create(
            name=f"Route for {customer}",
            waypoints=waypoints,
            distance_km=round(float(distance), 2),
            estimated_duration=duration
        )

        # Create order
        order = Order.objects.create(
            customer_name=customer,
            origin=origin,
            destination=destination,
            load_weight=load_weight,
            deadline=deadline,
            status=status,
            route=route
        )

        # Dispatcher validation
        dispatcher = Profile.objects.filter(id=dispatcher_id, role="dispatcher").first()
        if not dispatcher:
            return JsonResponse({"error": "Provided dispatcher not found or invalid"}, status=400)

        # Driver validation
        driver = Driver.objects.get(id=driver_id, availability=True)
        if Trip.objects.filter(driver=driver, end_time__isnull=True).exists():
            return JsonResponse({"error": "Driver already has an active trip"}, status=400)
        driver_profile = Profile.objects.get(user=driver.user, role="driver")

        # Get trip and validate
        trip = Trip.objects.get(id=trip_id)

        # Get optimal vehicle
        optimal_vehicle = get_optimal_vehicle_only()
        if not optimal_vehicle:
            return JsonResponse({"error": "No available vehicle found"}, status=400)

        # Ensure trip vehicle matches selected optimal vehicle
        if trip.vehicle != optimal_vehicle:
            return JsonResponse({
                "error": f"Trip vehicle (ID {trip.vehicle.id}) does not match optimal vehicle (ID {optimal_vehicle.id})"
            }, status=400)

        # Create dispatch task
        DispatchTask.objects.create(
            dispatcher=dispatcher,
            driver=driver_profile,
            vehicle=optimal_vehicle,
            route=route,
            trip=trip
        )

        driver.availability = False
        driver.save()
        optimal_vehicle.status = 'inactive'
        optimal_vehicle.save()
        return JsonResponse({
            "message": "Order and dispatch mapped successfully",
            "order_id": order.id,
            "trip_id": trip.id,
            "vehicle_id": optimal_vehicle.id,
            "driver_id": driver_profile.id,
            "dispatcher_id": dispatcher.id,
            "route_id": route.id
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@csrf_protect
@require_http_methods(["POST"])
def cancel_order(request):
    try:
        data = json.loads(request.body)
        order_id = data.get("order_id")

        order = get_object_or_404(Order, id=order_id)
        dispatch = DispatchTask.objects.filter(route=order.route).first()

        if dispatch:
            # Optional: revert statuses
            driver_profile = dispatch.driver
            vehicle = dispatch.vehicle

            try:
                driver = Driver.objects.get(user=driver_profile.user)
                driver.availability = True
                driver.save()
            except Driver.DoesNotExist:
                pass

            vehicle.status = 'active'
            vehicle.save()

            # Remove dispatch task
            dispatch.delete()

        order.status = "cancelled"
        order.save()

        return JsonResponse({"message": "Order cancelled and resources released."}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@csrf_protect
@require_http_methods(["POST"])
def complete_order(request):
    try:
        data = json.loads(request.body)
        order_id = data.get("order_id")

        order = get_object_or_404(Order, id=order_id)
        dispatch = DispatchTask.objects.filter(route=order.route).first()

        if dispatch:
            driver_profile = dispatch.driver
            vehicle = dispatch.vehicle

            # Set driver availability = True
            driver = Driver.objects.get(user=driver_profile.user)
            driver.availability = True
            driver.save()

            # Set vehicle status = 'active'
            vehicle.status = 'active'
            vehicle.save()

        order.status = "completed"
        order.save()

        return JsonResponse({"message": "Order marked as completed, driver and vehicle released."}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
