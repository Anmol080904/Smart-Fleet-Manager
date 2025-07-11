# dispatcher/models.py
from django.db import models
from vehicles.models import Vehicle
from users.models import Profile
from routes.models import Route
from trips.models import Trip

class DispatchTask(models.Model):
    dispatcher = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'dispatcher'})
    driver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='assigned_tasks', limit_choices_to={'role': 'driver'})
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task {self.id} by {self.dispatcher.user.username}"