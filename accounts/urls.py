from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from vehicles import views as vehicle_views  # ✅ import staff dashboard from vehicles app

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('dashboard/admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/staff/', vehicle_views.staff_dashboard, name='staff_dashboard'),  # ✅ now points to vehicles.views.staff_dashboard

    # User management (admin only)
    path('users/manage/', views.manage_users_view, name='manage_users'),
    path('users/create/', views.create_user_view, name='create_user'),
    path('users/edit/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),

    # Driver registration (old standalone page — still works if needed)
    path('driver/register/', views.driver_registration, name='driver_registration'),
    path('driver/register/success/', views.driver_registration_success, name='driver_registration_success'),
]
