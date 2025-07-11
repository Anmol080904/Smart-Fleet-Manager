from django.urls import path
from .views import register_user, login_user, logout_user, list_profiles, get_csrf_token

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('users/', list_profiles, name='user-list'),
    path('csrf/', get_csrf_token, name='csrf'),
]
