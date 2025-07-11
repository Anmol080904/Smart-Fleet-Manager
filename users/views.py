import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.middleware.csrf import get_token
from .models import Profile

@csrf_protect
@require_http_methods(["POST"])
def register_user(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        email = data['email']
        password = data['password']
        role = data.get('role', 'dispatcher')
        company=data.get('company')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        if role == 'admin':
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

        Profile.objects.create(user=user, role=role,company=company)
        return JsonResponse({'message': 'User registered successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_protect
@require_http_methods(["POST"])
def login_user(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'username': user.username,
                'email': user.email,
                'role': user.profile.role,
                'company':user.profile.company
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
def logout_user(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'}, status=200)

@require_http_methods(["GET"])
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)}, status=200)

@require_http_methods(["GET"])
def list_profiles(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        return JsonResponse({'error': 'Forbidden'}, status=403)

    profiles = Profile.objects.select_related('user').all()
    profile_data = []

    for profile in profiles:
        profile_data.append({
            'id': profile.id,
            'user_id': profile.user.id,
            'username': profile.user.username,
            'email': profile.user.email,
            'role': profile.role,
            'company':profile.company,
        })

    return JsonResponse(profile_data, safe=False, status=200)

@csrf_protect
@require_http_methods(["POST"])
def delete_profile(request):
    if not request.user.is_authenticated or request.user.profile.role != 'admin':
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        user = User.objects.get(id=user_id)

        if user.is_superuser:
            return JsonResponse({'error': 'Cannot delete superuser'}, status=403)

        user.delete()
        return JsonResponse({'message': 'Profile and associated user deleted successfully'}, status=200)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
