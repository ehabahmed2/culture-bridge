from django.db import models
from Users.models import CustomUser
from django.contrib.sessions.models import Session

# Moderls' fields we need to create
# - User (if authenticated, otherwise null)

# - Session key (for anonymous users)

# - Feedback text

# - Rating (optional)

# - Timestamp

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL,null=True, blank=True,)
    
    # text input and output of transalation
    input_text = models.TextField(blank=True, null=True)
    output_text = models.TextField(blank=True, null=True)
    dialect = models.CharField(max_length=200, blank=True, null=True)
    
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])# let user rate from 1-5
    comments = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        verbose_name_plural = "Feedback"
        ordering = ['-created_at']