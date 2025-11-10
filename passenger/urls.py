# passenger/urls.py
from django.urls import path
from . import views

app_name = 'passenger'

urlpatterns = [
    path('', views.public_queue_view, name='public_queue'),
]
