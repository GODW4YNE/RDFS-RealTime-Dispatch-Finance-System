from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from django.shortcuts import redirect

urlpatterns = [
    # ✅ Default route: redirect to Passenger Public Page (public landing for now)
    path('', lambda request: redirect('passenger:home')),

    # 🔒 Hidden Django admin site (only accessible to authorized people)
    path('super-secret-admin/', admin.site.urls),

    # ✅ Include all app routes
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('vehicles/', include(('vehicles.urls', 'vehicles'), namespace='vehicles')),
    path('terminal/', include(('terminal.urls', 'terminal'), namespace='terminal')),
    path('reports/', include(('reports.urls', 'reports'), namespace='reports')),

    # ✅ Passenger app (public access)
    path('passenger/', include(('passenger.urls', 'passenger'), namespace='passenger')),

    # ✅ Explicit dashboard shortcuts (still fine for logged-in users)
    path('dashboard/admin/', accounts_views.admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/staff/', accounts_views.staff_dashboard_view, name='staff_dashboard'),
]

# ✅ Media support during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
