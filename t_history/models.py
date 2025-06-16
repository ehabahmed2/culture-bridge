from django.db import models
from Users.models import CustomUser
from django.utils import timezone
# Create your models here.

class TransalationHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    input_text = models.TextField()
    output_text = models.TextField()
    target_culture = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime(('%Y-%m-%d %H:%M'))}"
    