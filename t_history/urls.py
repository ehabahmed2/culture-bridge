from django.urls import path
from . import views

urlpatterns = [
    path('', views.translation_history, name='history'),
    path('delete_history/', views.delete_history, name='delete_history'),  

]
