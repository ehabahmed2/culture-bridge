from django.urls import path
from . import views

urlpatterns = [
    path('', views.plans, name='plans'),
    path('payment/', views.payment, name='payment'),
]
