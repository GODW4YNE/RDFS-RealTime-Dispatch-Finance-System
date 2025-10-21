from django.urls import path
from . import views

urlpatterns = [
    path('deposit-menu/', views.deposit_menu, name='deposit_menu'),
    path('queue/', views.terminal_queue, name='terminal_queue'),
]
