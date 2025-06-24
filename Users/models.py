from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=200)
    credits = models.PositiveIntegerField(default=100)
    email = models.EmailField(unique=True)
    
    store_history = models.BooleanField(default=False)
    consent_date = models.DateTimeField(null=True, blank=True)
    
    # check last credit update
    last_credit_update = models.DateField(default=timezone.now)
    def __str__(self):
        return self.username