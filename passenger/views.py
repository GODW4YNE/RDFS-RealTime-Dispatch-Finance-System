# passenger/views.py
from django.shortcuts import render
from terminal.models import EntryLog
from vehicles.models import Vehicle

def public_queue_view(request):
    """
    Public Passenger View:
    - Shows all active vehicles currently inside the terminal.
    - Allows passengers to filter vehicles by route.
    - No login required.
    """

    # ✅ Get filter query for route
    route_filter = request.GET.get('route')

    # ✅ Collect distinct routes from active vehicles
    routes = (
        Vehicle.objects.filter(entry_logs__is_active=True)
        .values_list('route', flat=True)
        .distinct()
    )

    # Base queryset: all active entry logs (vehicles currently inside)
    queue_entries = (
        EntryLog.objects.select_related('vehicle', 'vehicle__assigned_driver')
        .filter(is_active=True)
        .order_by('created_at')
    )

    # ✅ Filter if passenger selects a route
    if route_filter and route_filter != 'all':
        queue_entries = queue_entries.filter(vehicle__route=route_filter)

    context = {
        'queue_entries': queue_entries,
        'routes': routes,
        'selected_route': route_filter,
    }

    return render(request, 'passenger/public_queue.html', context)
