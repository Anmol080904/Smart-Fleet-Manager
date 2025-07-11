from django.urls import path
from .views import (
    list_dispatch_tasks
)

urlpatterns = [
    path('list/', list_dispatch_tasks, name='create-dispatch'),
   
]
