from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('profit-report/', views.profit_report_view, name='profit_report'),
]
