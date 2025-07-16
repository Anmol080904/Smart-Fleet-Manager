from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('dispatcher', 'Dispatcher'),
        ('driver', 'Driver'),
        ('accountant', 'Accountant'),
        ('customer','Customer')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='dispatcher')
    company=models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return f"{self.user.username} ({self.role})"
