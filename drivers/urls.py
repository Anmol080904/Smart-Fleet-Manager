from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_driver, name='create-driver'),
    path('list/', views.list_drivers, name='list-drivers'),
    path('update/<int:driver_id>/', views.update_driver, name='update-driver'),
    path('delete/<int:driver_id>/', views.delete_driver, name='delete-driver'),
    path('change-status/',views.toggle_availability,name='Status change'),
]
