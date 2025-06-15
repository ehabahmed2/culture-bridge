from django.contrib import admin
from Users.models import CustomUser
from django.contrib.auth.admin import UserAdmin  # Import the default UserAdmin

# Register your models here.
admin.site.register(CustomUser)