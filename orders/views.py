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

        # Create order without dispatcher, driver, or trip
        order = Order.objects.create(
            customer_name=customer,
            origin=origin,
            destination=destination,
            load_weight=load_weight,
            deadline=deadline,
            status=status,
            route=route
        )

        return JsonResponse({
            "message": "Order created. Awaiting dispatcher assignment.",
            "order_id": order.id,
            "route_id": route.id
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
