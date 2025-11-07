from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from vehicles.models import Driver, Vehicle
from terminal.models import EntryLog


# ✅ Role checkers
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, 'role', '') == 'admin')


def is_staff_admin(user):
    return user.is_authenticated and (user.is_staff or getattr(user, 'role', '') == 'staff_admin')


# ✅ LOGIN VIEW
@never_cache
def login_view(request):
    # Always flush session when visiting login page (security)
    request.session.flush()

    # If user is already logged in, redirect based on role
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('accounts:admin_dashboard')
        elif is_staff_admin(request.user):
            return redirect('accounts:staff_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['role'] = getattr(user, 'role', '')

            if is_admin(user):
                return redirect('accounts:admin_dashboard')
            elif is_staff_admin(user):
                return redirect('accounts:staff_dashboard')
            else:
                messages.error(request, "Access denied. Only admins and staff can access this system.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')


# ✅ LOGOUT VIEW
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
    total_drivers = Driver.objects.count()
    total_vehicles = Vehicle.objects.count()
    total_queue = EntryLog.objects.filter(status=EntryLog.STATUS_SUCCESS).count()
    total_profit = 0

    drivers = Driver.objects.all().order_by('last_name')
    vehicles = Vehicle.objects.select_related('assigned_driver').order_by('license_plate')

    context = {
        'total_drivers': total_drivers,
        'total_vehicles': total_vehicles,
        'total_queue': total_queue,
        'total_profit': total_profit,
        'drivers': drivers,
        'vehicles': vehicles,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


# ✅ STAFF DASHBOARD
@login_required(login_url='login')
@user_passes_test(is_staff_admin)
@never_cache
def staff_dashboard_view(request):
    total_drivers = Driver.objects.count()
    total_vehicles = Vehicle.objects.count()

    context = {
        'total_drivers': total_drivers,
        'total_vehicles': total_vehicles,
        'register_driver_url': 'vehicles:register_driver',
        'register_vehicle_url': 'vehicles:register_vehicle',
        'deposit_menu_url': 'terminal:deposit_menu',
    }
    return render(request, 'accounts/staff_dashboard.html', context)


# ✅ MANAGE USERS
@login_required(login_url='login')
@user_passes_test(is_admin)
@never_cache
def manage_users(request):
    return render(request, "accounts/manage_users.html")


@login_required(login_url='login')
@user_passes_test(is_admin)
@never_cache
def create_user(request):
    """Temporary placeholder for creating staff/admin accounts"""
    return render(request, "accounts/create_user.html")
