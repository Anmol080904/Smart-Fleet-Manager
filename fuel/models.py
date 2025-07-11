from django.db import models
from vehicles.models import Vehicle

class FuelLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_logs')
    date = models.DateField()
    quantity = models.FloatField(help_text="Liters")
    cost = models.FloatField(help_text="Total cost for this refueling")
    def __str__(self):
        return f"{self.vehicle.license_plate} - Fuel on {self.date}"