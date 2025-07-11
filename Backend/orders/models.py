# models.py (Order)
from django.db import models
from routes.models import Route  # adjust import as needed

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    customer_name = models.CharField(max_length=100)
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    load_weight = models.FloatField()
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)  # added field

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
