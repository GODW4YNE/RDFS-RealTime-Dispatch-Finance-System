from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from vehicles.models import Vehicle, Wallet, Driver, Deposit  # 🟩 Added models
from .models import EntryLog
from decimal import Decimal


# 🔐 Helper: Check if user is staff
def is_staff_admin(user):
    return user.is_authenticated and (user.is_staff or getattr(user, 'role', '') == 'staff_admin')


# ✅ Deposit Menu View (Fixed)
@login_required(login_url='login')
@user_passes_test(is_staff_admin)
@never_cache
def deposit_menu(request):
    """
    Allows staff to select a driver (only those with registered vehicles),
    view wallet balance, and record deposits.
    """
    # 🟩 Only drivers who have at least one registered vehicle (corrected)
    drivers_with_vehicles = Driver.objects.filter(vehicles__isnull=False).distinct().order_by('last_name', 'first_name')

    # 🟩 Get recent deposits (limit 10)
    recent_deposits = (
        Deposit.objects
        .select_related('wallet__vehicle__assigned_driver')
        .order_by('-created_at')[:10]
    )

    context = {
        "drivers": drivers_with_vehicles,
        "recent_deposits": recent_deposits,
    }

    return render(request, "terminal/deposit_menu.html", context)


# ✅ Terminal Queue View
@login_required(login_url='login')
@user_passes_test(is_staff_admin)
@never_cache
def terminal_queue(request):
    """Displays live queue of recent validated vehicle entries."""
    return render(request, 'terminal/terminal_queue.html')


# 🆕 STEP 3.5: AJAX endpoint — Live Queue Data
@login_required(login_url='login')
@user_passes_test(is_staff_admin)
@never_cache
def queue_data(request):
    """
    Returns the latest EntryLog records as JSON for live queue refresh.
    Used by terminal_queue.html to auto-update every few seconds.
    """
    logs = (
        EntryLog.objects
        .filter(status=EntryLog.STATUS_SUCCESS)
        .select_related("vehicle", "staff")
        .order_by("-created_at")[:20]
    )

    data = []
    for log in logs:
        vehicle = log.vehicle
        data.append({
            "vehicle_plate": getattr(vehicle, "plate_number", "N/A") if vehicle else "—",
            "driver_name": getattr(vehicle.driver, "name", "N/A") if vehicle and hasattr(vehicle, "driver") else "—",
            "fee": float(log.fee_charged),
            "staff": log.staff.username if log.staff else "—",
            "time": log.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return JsonResponse({"entries": data})


# 🟩 STEP 2.2: QR Scan Entry Validation + Enhanced Error Feedback
@login_required(login_url='login')
@user_passes_test(is_staff_admin)
@never_cache
def qr_scan_entry(request):
    """
    Handles QR scans from the camera and provides clear feedback.
    Deducts entry fee if balance is sufficient.
    Prevents double entry if vehicle is already in queue.
    """
    if request.method == "POST":
        qr_code = request.POST.get("qr_code", "").strip()
        if not qr_code:
            return JsonResponse({"status": "error", "message": "QR code is empty. Please try again."})

        entry_fee = Decimal("10.00")
        staff_user = request.user

        try:
            # 🔍 Look for matching vehicle QR
            vehicle = Vehicle.objects.filter(qr_code=qr_code).first()
            if not vehicle:
                return JsonResponse({
                    "status": "error",
                    "message": "No vehicle found for this QR code. Please make sure it's valid."
                })

            # 🚫 Prevent duplicate queue entry
            from .models import EntryLog
            recent_entry = EntryLog.objects.filter(
                vehicle=vehicle,
                status=EntryLog.STATUS_SUCCESS
            ).order_by('-created_at').first()

            if recent_entry:
                # If the last log is recent (within 5 minutes), prevent re-entry
                from datetime import timedelta, timezone, datetime
                now = datetime.now(timezone.utc)
                if (now - recent_entry.created_at) < timedelta(minutes=5):
                    return JsonResponse({
                        "status": "error",
                        "message": f"Driver for vehicle '{vehicle.plate_number}' is already in queue."
                    })

            wallet = Wallet.objects.filter(vehicle=vehicle).first()
            if not wallet:
                return JsonResponse({
                    "status": "error",
                    "message": "No wallet found for this vehicle. Please register deposit first."
                })

            # ✅ Sufficient balance
            if wallet.balance >= entry_fee:
                wallet.balance -= entry_fee
                wallet.save()

                EntryLog.objects.create(
                    vehicle=vehicle,
                    staff=staff_user,
                    fee_charged=entry_fee,
                    status=EntryLog.STATUS_SUCCESS,
                    message=f"Vehicle '{vehicle.plate_number}' validated. ₱{entry_fee} deducted."
                )

                return JsonResponse({
                    "status": "success",
                    "message": f"✅ Vehicle '{vehicle.plate_number}' validated successfully! ₱{entry_fee} deducted."
                })

            else:
                EntryLog.objects.create(
                    vehicle=vehicle,
                    staff=staff_user,
                    fee_charged=entry_fee,
                    status=EntryLog.STATUS_INSUFFICIENT,
                    message=f"Insufficient balance for vehicle '{vehicle.plate_number}'."
                )
                return JsonResponse({
                    "status": "error",
                    "message": f"❌ Insufficient balance for vehicle '{vehicle.plate_number}'. Please deposit funds."
                })

        except Exception as e:
            # ✅ Catch all unexpected issues safely
            return JsonResponse({
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            })

    # GET request → just load the scan page
    return render(request, "terminal/qr_scan_entry.html")
