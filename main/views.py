from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

#from django.shortcuts import render
#from .models import Trip

# Create your views here.
#from django.shortcuts import render

#def home(request):
#    return render(request, 'base.html')

#def view_available_trips(request):
#    available_trips = Trip.objects.filter(status='Scheduled')
#    context = {'trips': available_trips}
#    return render(request, 'available_trips.html', context)
