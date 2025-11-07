from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views

urlpatterns = [
    # ✅ Default route: always goes to login page
    path('', accounts_views.login_view, name='login'),

    # ✅ Django admin site
    path('admin/', admin.site.urls),

    # ✅ Include all app routes with namespaces
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('vehicles/', include(('vehicles.urls', 'vehicles'), namespace='vehicles')),
    path('terminal/', include(('terminal.urls', 'terminal'), namespace='terminal')),
    path('reports/', include(('reports.urls', 'reports'), namespace='reports')),

    # ✅ Explicit dashboard shortcuts (still work fine)
    path('dashboard/admin/', accounts_views.admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/staff/', accounts_views.staff_dashboard_view, name='staff_dashboard'),
]

# ✅ Media support during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
