# reports/views.py
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import datetime
from accounts.models import CustomUser
from .models import Profit
from accounts.utils import is_admin  # if you already have this helper

@login_required(login_url='login')
@user_passes_test(is_admin)
def profit_report_view(request):
    """
    Displays profit records with total and optional date range filtering.
    Accessible only to Admin users.
    """
    profits = Profit.objects.all().order_by('-date_recorded')
    total = profits.aggregate(Sum('amount'))['amount__sum'] or 0

    # --- Optional: Date Range Filtering ---
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_dt = timezone.make_aware(datetime.combine(end_dt, datetime.max.time()))
            start_dt = timezone.make_aware(datetime.combine(start_dt, datetime.min.time()))
            profits = profits.filter(date_recorded__range=[start_dt, end_dt])
            total = profits.aggregate(Sum('amount'))['amount__sum'] or 0
        except ValueError:
            pass  # Ignore invalid date input

    context = {
        'profits': profits,
        'total': total,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'reports/profit_report.html', context)
