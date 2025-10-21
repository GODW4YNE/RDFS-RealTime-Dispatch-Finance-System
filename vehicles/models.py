import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
import re
from django.core.exceptions import ValidationError
import uuid
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Driver(models.Model):
    driver_id = models.CharField(max_length=100, unique=True, default="", blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=150, blank=True, null=True)
    blood_type = models.CharField(max_length=5, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    house_number = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    barangay = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city_municipality = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=20, blank=True, null=True)
    license_expiry = models.DateField(blank=True, null=True)
    license_type = models.CharField(max_length=20, blank=True, null=True)
    license_image = models.ImageField(upload_to='licenses/', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.driver_id:
            self.driver_id = f"DRV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.driver_id})"


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('jeepney', 'Jeepney'),
        ('bus', 'Bus'),
        ('van', 'Van'),
        ('tricycle', 'Tricycle'),
        ('taxi', 'Taxi'),
    ]

    OWNERSHIP_TYPES = [
        ('owned', 'Owned'),
        ('leased', 'Leased'),
        ('private', 'Private'),
    ]

    vehicle_name = models.CharField(max_length=100, default="Unnamed Vehicle")
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPES)
    ownership_type = models.CharField(max_length=20, choices=OWNERSHIP_TYPES, default='owned')
    assigned_driver = models.ForeignKey('Driver', on_delete=models.CASCADE, related_name='vehicles')

    # 🔹 Registration details
    cr_number = models.CharField(max_length=50, unique=True, verbose_name="Certificate of Registration")
    or_number = models.CharField(max_length=50, unique=True, verbose_name="Official Receipt")
    vin_number = models.CharField(max_length=50, unique=True, verbose_name="Vehicle Identification Number (VIN)")
    year_model = models.PositiveIntegerField(default=2024)

    # 🔹 Vehicle info
    registration_number = models.CharField(max_length=50, unique=True)
    registration_expiry = models.DateField(blank=True, null=True)
    license_plate = models.CharField(max_length=50, unique=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    seat_capacity = models.PositiveIntegerField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)

    # 🔹 Auto timestamps
    date_registered = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        """Validate license plate format (e.g., ABC 123)."""
        if self.license_plate and not re.match(r'^[A-Z]{3}\s\d{3,4}$', self.license_plate, re.IGNORECASE):
            raise ValidationError("License plate must be in format XXX 123 or XXX 1234 (e.g., ABC 123).")

    def save(self, *args, **kwargs):
        """Generate QR code only after creating the vehicle."""
        creating = self.pk is None
        super().save(*args, **kwargs)

        # Only generate QR once when new
        if creating and not self.qr_code:
            qr_content = (
                f"VEHICLE ID: {self.id}\n"
                f"NAME: {self.vehicle_name}\n"
                f"TYPE: {self.get_vehicle_type_display()}\n"
                f"PLATE: {self.license_plate}\n"
                f"DRIVER: {self.assigned_driver}\n"
                f"CR: {self.cr_number}\n"
                f"OR: {self.or_number}\n"
                f"VIN: {self.vin_number}\n"
                f"YEAR: {self.year_model}"
            )

            qr_image = qrcode.make(qr_content)
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            filename = f"vehicle_{self.id}_qr.png"
            self.qr_code.save(filename, File(buffer), save=False)
            super().save(update_fields=['qr_code'])

    def __str__(self):
        return f"{self.vehicle_name} ({self.license_plate})"


class Wallet(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
    ]

    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='PHP')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle.assigned_driver}'s Wallet - {self.balance} {self.currency}"


class Deposit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('manual', 'Manual Payment (In-Station)'),
        ('online', 'Online Payment'),
        ('bank_transfer', 'Bank Transfer'),
        ('gcash', 'GCash'),
        ('maya', 'Maya'),
    ]

    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='manual')
    reference_number = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Auto-generate reference number and set status automatically."""
        is_new = self.pk is None

        if not self.reference_number:
            unique_code = uuid.uuid4().hex[:6].upper()
            self.reference_number = f"DEP-{timezone.now().strftime('%Y%m%d')}-{unique_code}"

        if not self.status:
            if self.payment_method in ['manual', 'bank_transfer']:
                self.status = 'pending'
            elif self.payment_method in ['gcash', 'maya', 'online']:
                self.status = 'successful'
            else:
                self.status = 'failed'

        super().save(*args, **kwargs)

        if is_new and self.status == 'successful':
            self.wallet.balance += self.amount
            self.wallet.save()

    def __str__(self):
        return f"Deposit {self.reference_number} - {self.amount} ({self.status})"


# 🔔 SIGNALS
@receiver(post_save, sender=Vehicle)
def create_wallet_for_vehicle(sender, instance, created, **kwargs):
    """Auto-create a wallet once a Vehicle is created."""
    if created:
        Wallet.objects.create(vehicle=instance)
