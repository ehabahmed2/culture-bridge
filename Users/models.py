from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=200)
    credits = models.PositiveIntegerField(default=100)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username