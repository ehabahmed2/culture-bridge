from django.utils import timezone
from .models import CustomUser

class DailyCreditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request only for authenticated users
        if request.user.is_authenticated and isinstance(request.user, CustomUser):
            user = request.user
            today = timezone.now().date()
            
            # Check if credits were updated today
            if user.last_credit_update < today:
                user.credits += 10
                user.last_credit_update = today
                user.save(update_fields=['credits', 'last_credit_update'])
        
        response = self.get_response(request)
        return response
    
# This middleware checks if the user is authenticated and updates their credits daily.
# It adds 10 credits if the last update was before today and saves the changes.