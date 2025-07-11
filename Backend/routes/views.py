import os
import json
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from .utils import fetch_route_from_ors, haversine_distance
from .models import Route


@csrf_protect
@require_http_methods(["POST"])
def create_route(request):
    try:
        data = json.loads(request.body)

        start = data.get('start')  # format: "lat,lon"
        end = data.get('end')      # format: "lat,lon"

        if not start or not end:
            return JsonResponse({'error': 'Start and end coordinates are required'}, status=400)

        try:
            start_coords = tuple(map(float, start.split(',')))
            end_coords = tuple(map(float, end.split(',')))
        except ValueError:
            return JsonResponse({'error': 'Invalid coordinate format. Use "lat,lon"'}, status=400)

        api_key = os.environ.get("ORS_API_KEY")
        if not api_key:
            return JsonResponse({'error': 'ORS API key not set in environment'}, status=500)

        waypoints, distance, duration = fetch_route_from_ors(start_coords, end_coords, api_key)

        # Fallback to Haversine if ORS fails or distance is zero
        if not waypoints or not isinstance(distance, (int, float)) or distance == 0:
            distance = haversine_distance(*start_coords, *end_coords)
            duration = timedelta(hours=distance / 40)  # average 40 km/h
            waypoints = [
                {"lat": start_coords[0], "lng": start_coords[1]},
                {"lat": end_coords[0], "lng": end_coords[1]}
            ]

        distance = float(distance)  # Ensure it's a float before rounding

        route = Route.objects.create(
            name=f"Route from {start} to {end}",
            waypoints=waypoints,
            distance_km=round(distance, 2),
            estimated_duration=duration
        )

        return JsonResponse({
            "message": "Route created",
            "id": route.id,
            "distance_km": round(distance, 2),
            "estimated_duration": str(duration),
            "waypoints": waypoints
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
