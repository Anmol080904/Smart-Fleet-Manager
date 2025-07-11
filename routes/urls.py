from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_route, name='create-route'),
    # path('list/', views.list_routes, name='list-routes'),
    # path('delete/<int:route_id>/', views.delete_route, name='delete-route'),
    # path('calculate-distance/', views.calculate_distance, name='calculate-distance'),
]
