from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount =models.PositiveIntegerField()
    
    # Add choices for transaction types
    TRANSACTION_TYPES = (
        ('purchase', 'Credit Purchase'),
        ('renewal', 'Daily Renewal'),
        ('usage', 'Translation Usage'),
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        default='purchase'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    description=models.CharField(max_length=200)
    
    
    # Useful for admin and debugging
    def __str__(self):
        return f"{self.user.email}: {self.amount} credits ({self.get_transaction_type_display()})"

    