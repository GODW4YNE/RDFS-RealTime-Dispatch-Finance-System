from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Staff Dashboard
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),

    # 🔹 Staff Registration Pages
    path('register-driver/', views.register_driver, name='register_driver'),
    path('register-vehicle/', views.register_vehicle, name='register_vehicle'),

    # 🔹 Standalone / Legacy Vehicle Registration
    path('register-vehicle-old/', views.vehicle_registration, name='register_vehicle_old'),

    # 🔹 OCR Endpoint for Driver License Scanning
    path('ocr-process/', views.ocr_process, name='ocr_process'),

    # 🔹 AJAX Endpoints
    path('ajax-register-driver/', views.ajax_register_driver, name='ajax_register_driver'),
    path('ajax-register-vehicle/', views.ajax_register_vehicle, name='ajax_register_vehicle'),
]
