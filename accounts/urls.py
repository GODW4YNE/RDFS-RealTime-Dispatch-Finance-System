from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from vehicles import views as vehicle_views  # ✅ import staff dashboard from vehicles app

urlpatterns = [
    # ✅ Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ✅ Dashboards
    path('dashboard/admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/staff/', vehicle_views.staff_dashboard, name='staff_dashboard'),

    # 📴 Disabled old driver registration routes (now handled by vehicles app)
    # path('driver/register/', views.driver_registration, name='driver_registration'),
    # path('driver/register/success/', views.driver_registration_success, name='driver_registration_success'),
]
