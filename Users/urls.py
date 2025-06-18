from django.urls import path
from . import views


urlpatterns = [
    # use new logout view instead of Django’s default
    path('logout/', views.logout_keep_free_attempts, name='logout'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('user-info/', views.user_info, name='user_info'),
    path('enable_history/', views.enable_history_storage, name='enable_history_storage'),
]