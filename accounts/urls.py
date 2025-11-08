from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # ✅ Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # ✅ Dashboards
    path("dashboard/admin/", views.admin_dashboard_view, name="admin_dashboard"),
    path("dashboard/staff/", views.staff_dashboard_view, name="staff_dashboard"),

    # ✅ User Management (Admin Only)
    path("manage-users/", views.manage_users, name="manage_users"),
    path("manage-users/create/", views.create_user, name="create_user"),
    path("manage-users/edit/<int:user_id>/", views.edit_user, name="edit_user"),
    path("manage-users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
]
