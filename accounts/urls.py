from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/admin/", views.admin_dashboard_view, name="admin_dashboard"),
    path("manage-users/", views.manage_users, name="manage_users"),
    path("create-user/", views.create_user, name="create_user"),  # 🆕 added
    path("dashboard/staff/", views.staff_dashboard_view, name="staff_dashboard"),
]
