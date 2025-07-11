from django.db import models
from vehicles.models import Vehicle
from django.contrib.auth.models import User

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry_date = models.DateField(null=True, blank=True)
    assigned_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='drivers')
    availability = models.BooleanField(default=True)

    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    joining_date = models.DateField(auto_now_add=True)
    experience_years = models.PositiveIntegerField()
    emergency_contact = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - {self.license_number}"
