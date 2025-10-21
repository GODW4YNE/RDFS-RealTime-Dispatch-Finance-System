from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache

# 🔐 Helper: Check if user is staff
def is_staff_admin(user):
    return user.is_authenticated and (user.is_staff or getattr(user, 'role', '') == 'staff_admin')

# ✅ Deposit Menu View
@login_required(login_url='login')
@user_passes_test(is_staff_admin)
@never_cache
def deposit_menu(request):
    # In the future, this will handle deposit logic for drivers.
    return render(request, 'terminal/deposit_menu.html')

# ✅ Terminal Queue View (Optional placeholder)
@login_required(login_url='login')
@user_passes_test(is_staff_admin)
@never_cache
def terminal_queue(request):
    return render(request, 'terminal/terminal_queue.html')
