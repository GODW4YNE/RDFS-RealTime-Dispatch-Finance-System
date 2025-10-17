from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test  # For protection
from .forms import DriverRegistrationForm

# Create your views here.
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'  # Assuming your CustomUser has a 'role' field

def is_staff_admin(user):
    return user.is_authenticated and user.role == 'staff_admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    return render(request, 'admin_dashboard.html')  # Render your admin dashboard template

@login_required
@user_passes_test(is_staff_admin)
def staff_dashboard_view(request):
    return render(request, 'staff_dashboard.html')  # Render your staff dashboard template


# Driver Registration View
def driver_registration(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            # Process the data
            # Here you would typically save to database
            # For now, we'll just print and redirect
            print("Driver registration data:", form.cleaned_data)
            return redirect('driver_registration_success')
    else:
        form = DriverRegistrationForm()
    
    return render(request, 'driver_registration.html', {'form': form})

def driver_registration_success(request):
    return render(request, 'registration_success.html', {'message': 'Driver registration submitted successfully!'})