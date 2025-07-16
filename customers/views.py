# orders/views_customer.py
import os
import json
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from orders.models import Order
from routes.models import Route
from routes.utils import fetch_route_from_ors, haversine_distance
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from .models import Customer
from django.contrib.auth.models import User
@csrf_protect
@require_http_methods(["POST"])
def login_customer(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_protect
@require_http_methods(["POST"])
def logout_customer(request):
    try:
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@csrf_protect
@require_http_methods(["POST"])
def register_customer(request):
    try:
        data = json.loads(request.body)

        username = data['username']
        password = data['password']
        confirm_password = data['confirm_password']
        email = data['email']
        full_name = data['full_name']
        phone = data['phone']
        address_line1 = data['address_line1']
        address_line2 = data.get('address_line2', '')
        city = data['city']
        state = data['state']
        country = data['country']
        pincode = data['pincode']
        company_name = data.get('company_name', '')

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)

        Customer.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
            company_name=company_name
        )

        return JsonResponse({'message': 'Customer registered successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@csrf_protect
@require_http_methods(["POST"])
def create_order(request):
    try:
        data = json.loads(request.body)
        customer = data['customer_name']
        origin = data['origin']  # this should be "lat,lon" string from frontend
        destination_lat = data['destination_lat']
        destination_lng = data['destination_lng']
        load_weight = data['load_weight']
        deadline = data['deadline']
        status = data.get('status', 'pending')
        start_coords = tuple(map(float, origin.split(',')))
        end_coords = (float(destination_lat), float(destination_lng))  # <-- From frontend
        api_key = os.environ.get("ORS_API_KEY")
        waypoints, distance, duration = fetch_route_from_ors(start_coords, end_coords, api_key)

        if not waypoints or not isinstance(distance, (int, float)):
            distance = haversine_distance(*start_coords, *end_coords)
            duration = timedelta(hours=distance / 40)
            waypoints = [
                {"lat": start_coords[0], "lng": start_coords[1]},
                {"lat": end_coords[0], "lng": end_coords[1]}
            ]

        destination = f"{destination_lat},{destination_lng}"

        route = Route.objects.create(
            name=f"Route for {customer}",
            waypoints=waypoints,
            distance_km=round(float(distance), 2),
            estimated_duration=duration
        )

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
            "message": "Order created successfully. Awaiting dispatcher assignment.",
            "order_id": order.id,
            "route_id": route.id
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from dispatcher.models import DispatchTask
from drivers.models import Driver
from django.shortcuts import get_object_or_404

@csrf_protect
@require_http_methods(["POST"])
def cancel_order_by_customer(request):
    try:
        data = json.loads(request.body)
        order_id = data.get("order_id")
        customer_name = data.get("customer_name")

        order = get_object_or_404(Order, id=order_id, customer_name=customer_name)

        if order.status in ['cancelled', 'completed']:
            return JsonResponse({"message": f"Order already {order.status}."}, status=400)

        dispatch = DispatchTask.objects.filter(route=order.route).first()
        if dispatch:
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

            dispatch.delete()

        order.status = "cancelled"
        order.save()

        return JsonResponse({"message": "Order cancelled successfully."}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@csrf_protect
@require_http_methods(["GET"])
def check_order_status(request):
    try:
        order_id = request.GET.get("order_id")
        customer_name = request.GET.get("customer_name")

        if not order_id or not customer_name:
            return JsonResponse({"error": "Missing order_id or customer_name"}, status=400)

        order = get_object_or_404(Order, id=order_id, customer_name=customer_name)

        # Find associated trip via DispatchTask
        dispatch = DispatchTask.objects.filter(route=order.route).first()
        trip_status = None
        start_time = None
        end_time = None
        if dispatch and dispatch.trip:
            trip = dispatch.trip
            trip_status = trip.status
            start_time = trip.start_time
            end_time = trip.end_time

        return JsonResponse({
            "order_id": order.id,
            "order_status": order.status,
            "trip_status": trip_status,
            "trip_start_time": start_time,
            "trip_end_time": end_time,
            "driver": dispatch.driver.user.username if dispatch else None,
            "vehicle": dispatch.vehicle.license_plate if dispatch else None
        }, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)