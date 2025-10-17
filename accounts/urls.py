from django.urls import path
from . import views  # Import your views if you have custom ones
from django.contrib.auth.views import LoginView, LogoutView  # For login/logout if needed

urlpatterns = [
     path('driver/register/', views.driver_registration, name='driver_registration'),
    path('driver/success/', views.driver_registration_success, name='driver_registration_success'),
]