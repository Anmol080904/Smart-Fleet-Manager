from django.db import models

class Route(models.Model):
    name = models.CharField(max_length=100)
    waypoints = models.JSONField()  # List of lat-lng pairs [{"lat": ..., "lng": ...}, ...]
    distance_km = models.FloatField()
    estimated_duration = models.DurationField()

    def __str__(self):
        return self.name
