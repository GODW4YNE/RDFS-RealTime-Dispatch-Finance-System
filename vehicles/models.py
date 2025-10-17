import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
import re
from django.core.exceptions import ValidationError
import re
import uuid


class Driver(models.Model):

    driver_id = models.CharField(max_length=100, unique=True, default="", blank=True)
    
    # 🧍 Personal Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=150, blank=True, null=True)
    blood_type = models.CharField(max_length=5, blank=True, null=True)

    # 📞 Contact Information
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # 🏠 Address
    house_number = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    barangay = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city_municipality = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)

    # 🚘 License Info
    license_number = models.CharField(max_length=20, blank=True, null=True)
    license_expiry = models.DateField(blank=True, null=True)
    license_type = models.CharField(max_length=20, blank=True, null=True)
    license_image = models.ImageField(upload_to='licenses/', blank=True, null=True)

    # 🚨 Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.driver_id:
            self.driver_id = f"DRV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.driver_id})"



from django.db import models
from django.core.exceptions import ValidationError
from django.core.files import File
from io import BytesIO
import qrcode
import re

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

    # Basic Info
    vehicle_name = models.CharField(max_length=100, default="Unnamed Vehicle")
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPES)
    ownership_type = models.CharField(max_length=20, choices=OWNERSHIP_TYPES, default='owned')

    # Driver Assignment
    assigned_driver = models.ForeignKey('Driver', on_delete=models.CASCADE, related_name='vehicles')

    # Registration & Identification
    registration_number = models.CharField(max_length=50, unique=True)
    registration_expiry = models.DateField(blank=True, null=True)
    license_plate = models.CharField(max_length=50, unique=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)

    # Capacity & Specs
    seat_capacity = models.PositiveIntegerField(blank=True, null=True)

    # QR Code
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)

    # Metadata
    date_registered = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        data = (
            f"Vehicle Type: {self.get_vehicle_type_display()}\n"
            f"Name        : {self.vehicle_name}\n"
            f"Plate       : {self.license_plate}\n"
            f"Driver      : {self.assigned_driver}\n"
            f"Seats       : {self.seat_capacity}"
        )

        qr_img = qrcode.make(data)
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        filename = f"qr_{self.license_plate}.png"
        self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)


    def clean(self):
        """Validate license plate format (e.g., ABC 123)."""
        if not re.match(r'^[A-Z]{3}\s\d{3}$', self.license_plate, re.IGNORECASE):
            raise ValidationError("License plate must be in format XXX 123 (e.g., ABC 123).")

    def __str__(self):
        return f"{self.vehicle_name} ({self.license_plate})"
