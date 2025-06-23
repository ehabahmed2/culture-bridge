from django.urls import path
from . import views

urlpatterns = [
    path('', views.plans, name='plans'),
    path('payment/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
]
