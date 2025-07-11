from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register_vehicle, name='register-vehicle'),
    path('list/', views.list_vehicles, name='list-vehicles'),
    path('update/<int:vehicle_id>/', views.update_vehicle, name='update-vehicle'),
    path('delete/<int:vehicle_id>/', views.delete_vehicle, name='delete-vehicle'),
]
