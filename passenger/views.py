# passenger/views.py
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from terminal.models import EntryLog, SystemSettings
from vehicles.models import Vehicle, Route
from django.http import JsonResponse
from django.db.models import Q


def public_queue_view(request):
    """
    Public Passenger View:
    - Shows active vehicles inside the terminal.
    - Keeps departed entries visible for 5 minutes (for passengers).
    - Passes departure_duration_minutes to template.
    """
    # Query param for route filter
    route_filter = request.GET.get('route')

    # system settings (departure duration controlled by admin)
    settings = SystemSettings.get_solo()
    departure_duration = getattr(settings, "departure_duration_minutes", 30)

    # 5-minute grace window for showing departed entries to passengers
    keep_departed_for = timedelta(minutes=5)
    now = timezone.now()
    departed_cutoff = now - keep_departed_for

    # Base queryset: entries that are active OR departed within last 5 minutes
    queue_entries = (
        EntryLog.objects.select_related('vehicle', 'vehicle__assigned_driver', 'vehicle__route')
        .filter(
            # show either active ones or recently departed (within 5 min)
            (Q(is_active=True) | Q(departed_at__gte=departed_cutoff))
        )
        .order_by('created_at')
    )

    # Optional: filter by route if provided (route id)
    if route_filter and route_filter != 'all':
        queue_entries = queue_entries.filter(vehicle__route__id=route_filter)

    # Build context items with computed departure_time and flags
    entries = []
    for log in queue_entries:
        v = log.vehicle
        d = v.assigned_driver if v else None

        # compute departure_time based on admin setting
        departure_time = log.created_at + timedelta(minutes=departure_duration)
        # convert to local time string for template usage (client will parse)
        departure_time_local = timezone.localtime(departure_time)

        # whether this row is a recently departed (for showing greyed out)
        recently_departed = False
        if not log.is_active:
            # departed and within grace window
            if log.departed_at and log.departed_at >= departed_cutoff:
                recently_departed = True

        entries.append({
            "id": log.id,
            "vehicle": v,
            "driver": d,
            "departure_time": departure_time_local,       # timezone aware datetime
            "entry_time": timezone.localtime(log.created_at),
            "is_active": log.is_active,
            "recently_departed": recently_departed,
            "route": getattr(v.route, "name", None) if v and v.route else None,
        })

    # collect distinct routes for the route filter dropdown
    routes_qs = Vehicle.objects.filter(entry_logs__is_active=True).values_list('route', flat=True).distinct()
    # convert to actual Route objects if needed in template (we can fetch Route objects)
    from vehicles.models import Route
    routes = Route.objects.filter(id__in=[r for r in routes_qs if r])

    context = {
        'queue_entries': entries,
        'routes': routes,
        'selected_route': route_filter,
        'departure_duration_minutes': departure_duration,
        # provide current server time so client JS can calibrate (ISO string)
        'server_now': timezone.localtime(now),
    }

    return render(request, 'passenger/public_queue.html', context)


def public_queue_data(request):
    """AJAX endpoint that returns live queue data for smooth refresh."""
    from datetime import timedelta
    from django.utils import timezone
    from terminal.models import EntryLog, SystemSettings
    from vehicles.models import Route

    settings = SystemSettings.get_solo()
    departure_duration = getattr(settings, "departure_duration_minutes", 30)
    now = timezone.now()

    ten_mins_ago = now - timedelta(minutes=10)
    route_filter = request.GET.get("route", "all")

    queue_entries = (
        EntryLog.objects.select_related("vehicle", "vehicle__assigned_driver", "vehicle__route")
        .filter(
            status=EntryLog.STATUS_SUCCESS,
            created_at__gte=ten_mins_ago - timedelta(minutes=departure_duration),
        )
        .order_by("created_at")
    )

    if route_filter != "all":
        queue_entries = queue_entries.filter(vehicle__route_id=route_filter)

    data = []
    for q in queue_entries:
        v = q.vehicle
        departure_time = q.created_at + timedelta(minutes=departure_duration)
        is_boarding = q.is_active
        is_departed_recently = not q.is_active and q.departed_at and (now - q.departed_at <= timedelta(minutes=10))
        if is_boarding or is_departed_recently:
            data.append({
                "plate": v.license_plate,
                "driver": f"{v.assigned_driver.first_name} {v.assigned_driver.last_name}" if v.assigned_driver else "—",
                "route": f"{v.route.origin} → {v.route.destination}" if v.route else "—",
                "status": "Boarding" if is_boarding else "Departed",
                "departure": departure_time.strftime("%Y-%m-%d %H:%M:%S"),
            })

    return JsonResponse({"entries": data})