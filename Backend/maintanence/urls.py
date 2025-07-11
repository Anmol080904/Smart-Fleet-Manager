# maintenance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_maintenance, name='create-maintenance'),
    path('list/', views.list_maintenance, name='list-maintenance'),
    path('delete/<int:log_id>/', views.delete_maintenance, name='delete-maintenance'),
]
