from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test  # ✅ added user_passes_test
from django.views.decorators.cache import never_cache  # ✅ added never_cache import
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from vehicles.models import Driver, Vehicle, Wallet
from terminal.models import EntryLog, TerminalFeeBalance  # ✅ Updated - removed TerminalQueue


# ✅ ROLE CHECK HELPERS
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, 'role', '') == 'admin')


def is_staff_admin(user):
    return user.is_authenticated and (user.is_staff or getattr(user, 'role', '') == 'staff_admin')


# ✅ LOGIN & LOGOUT
def login_view(request):
    if not request.user.is_authenticated:
        request.session.flush()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if is_admin(user):
                login(request, user)
                request.session['role'] = 'admin'
                return redirect('admin_dashboard')
            elif is_staff_admin(user):
                login(request, user)
                request.session['role'] = 'staff_admin'
                return redirect('staff_dashboard')
            else:
                messages.error(request, "Access denied. Only admins and staff can access this system.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# ✅ ADMIN DASHBOARD
@login_required(login_url='login')
@user_passes_test(is_admin)
@never_cache
def admin_dashboard_view(request):
    """Admin dashboard — shows statistics and all registered drivers and vehicles."""
    total_drivers = Driver.objects.count() if Driver else 0
    total_vehicles = Vehicle.objects.count() if Vehicle else 0
    total_queue = EntryLog.objects.filter(status=EntryLog.STATUS_SUCCESS).count()  # ✅ replaced TerminalQueue
    total_profit = 0  # Placeholder — integrate with reports later

    # 🧩 SAFELY FETCH DRIVERS AND VEHICLES
    drivers = Driver.objects.all().order_by('last_name') if Driver else []
    vehicles = Vehicle.objects.select_related('assigned_driver').order_by('license_plate') if Vehicle else []

    # 🧩 GUARANTEE NON-NULL FIELDS
    for d in drivers:
        d.driver_id = d.driver_id or "N/A"
        d.first_name = d.first_name or ""
        d.last_name = d.last_name or ""
        d.license_number = d.license_number or "N/A"
        d.license_expiry = d.license_expiry or None
        d.mobile_number = d.mobile_number or "N/A"

    for v in vehicles:
        v.vehicle_name = v.vehicle_name or "Unnamed Vehicle"
        v.license_plate = v.license_plate or "N/A"
        v.vehicle_type_display = v.get_vehicle_type_display() if hasattr(v, "get_vehicle_type_display") else "N/A"
        v.ownership_display = v.get_ownership_type_display() if hasattr(v, "get_ownership_type_display") else "N/A"
        v.driver_name = (
            f"{v.assigned_driver.first_name} {v.assigned_driver.last_name}"
            if v.assigned_driver else "N/A"
        )

    context = {
        'total_drivers': total_drivers or 0,
        'total_vehicles': total_vehicles or 0,
        'total_queue': total_queue or 0,
        'total_profit': total_profit or 0,
        'drivers': drivers,
        'vehicles': vehicles,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


# ✅ STAFF DASHBOARD
@login_required(login_url='login')
@user_passes_test(is_staff_admin)
@never_cache
def staff_dashboard_view(request):
    """
    Staff dashboard — now serves as a hub linking to:
      - vehicles:register_driver
      - vehicles:register_vehicle
      - terminal:deposit_menu
    """
    total_drivers = Driver.objects.count() if Driver else 0
    total_vehicles = Vehicle.objects.count() if Vehicle else 0

    context = {
        'total_drivers': total_drivers,
        'total_vehicles': total_vehicles,
        # ✅ Add URLs for dashboard cards
        'register_driver_url': 'vehicles:register_driver',
        'register_vehicle_url': 'vehicles:register_vehicle',
        'deposit_menu_url': 'terminal:deposit_menu',
    }
    return render(request, 'accounts/staff_dashboard.html', context)
