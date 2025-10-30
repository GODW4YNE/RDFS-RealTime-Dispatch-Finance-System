from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class TerminalFeeBalance(models.Model):
    """
    Optional per-vehicle fee balance table.
    If your project already uses a Wallet model in vehicles app,
    you can keep this for compatibility or remove it later.
    """
    vehicle = models.OneToOneField(
        'vehicles.Vehicle',
        on_delete=models.CASCADE,
        related_name='fee_balance'
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def clean(self):
        if self.balance < 0:
            raise ValidationError("Balance cannot be negative.")

    def __str__(self):
        plate = getattr(self.vehicle, 'plate_number', None) or getattr(self.vehicle, 'license_plate', None)
        return f"Balance for {plate or self.vehicle.pk}"


class EntryLog(models.Model):
    """
    Records each QR validation attempt at the terminal.
    Useful for audits and troubleshooting.
    """
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'
    STATUS_INSUFFICIENT = 'insufficient'
    STATUS_INVALID = 'invalid'

    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Success'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_INSUFFICIENT, 'Insufficient Balance'),
        (STATUS_INVALID, 'Invalid QR'),
    ]

    vehicle = models.ForeignKey(
        'vehicles.Vehicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entry_logs'
    )
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='terminal_actions'
    )
    fee_charged = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_FAILED)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Entry Log"
        verbose_name_plural = "Entry Logs"

    def __str__(self):
        plate = getattr(self.vehicle, 'plate_number', None) or getattr(self.vehicle, 'license_plate', None)
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {plate or 'Unknown vehicle'} - {self.status}"
