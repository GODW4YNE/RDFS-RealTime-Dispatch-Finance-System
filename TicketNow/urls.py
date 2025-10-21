from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import login_view, admin_dashboard_view, staff_dashboard_view

urlpatterns = [
    # ✅ Default login page
    path('', login_view, name='login'),

    # ✅ Django admin site
    path('admin/', admin.site.urls),

    # ✅ Include app routes
    path('accounts/', include('accounts.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('terminal/', include('terminal.urls')),
    path('reports/', include('reports.urls')),

    # ✅ Correct dashboards (no more conflict with vehicles.urls)
    path('dashboard/admin/', admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/staff/', staff_dashboard_view, name='staff_dashboard'),
]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
