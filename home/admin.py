from django.contrib import admin
from Users.models import CustomUser
from django.contrib.auth.admin import UserAdmin  # Import the default UserAdmin
from t_history.models import TransalationHistory
from feedback.models import Feedback


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(TransalationHistory)
admin.site.register(Feedback)