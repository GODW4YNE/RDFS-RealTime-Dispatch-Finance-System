from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_home, name='reports_home'),  # 👈 Add this line if missing
    path('deposit-analytics/', views.deposit_analytics, name='deposit_analytics'),
    path('deposit-vs-revenue/', views.deposit_vs_revenue, name='deposit_vs_revenue'),
    path('profit-report/', views.profit_report_view, name='profit_report'),
]
