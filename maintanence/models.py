from django.db import models
from vehicles.models import Vehicle

class MaintenanceLog(models.Model):
    TYPE_CHOICES = [
        ('oil_change', 'Oil Change'),
        ('engine_check', 'Engine Check'),
        ('brake_service', 'Brake Service'),
        ('tire_rotation', 'Tire Rotation'),
        ('other', 'Other')
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_logs')
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True)
    cost = models.FloatField()
    km_at_service = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.type} on {self.date}"