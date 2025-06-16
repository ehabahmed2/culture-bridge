from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('translate/', views.translate_view, name='translate'),   
    path('save-translation/', views.save_translation, name='save_translation'),  

]
