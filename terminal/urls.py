# terminal/urls.py
from django.urls import path
from . import views

app_name = 'terminal'

urlpatterns = [
    # ✅ Staff deposit page
    path('deposit-menu/', views.deposit_menu, name='deposit_menu'),

    # ✅ Terminal queue page (main live page)
    path('queue/', views.terminal_queue, name='terminal_queue'),

    # ✅ QR Scan Entry page (Step 2)
    path('qr-scan-entry/', views.qr_scan_entry, name='qr_scan_entry'),

    # 🆕 AJAX endpoint for auto-refresh queue (Step 3.5)
    path('queue-data/', views.queue_data, name='queue_data'),
]
