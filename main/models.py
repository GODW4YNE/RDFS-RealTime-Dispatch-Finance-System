from django.db import models

class Trip(models.Model):
    """
    Links a trip record to an EntryLog instead of the old TerminalQueue.
    Each trip corresponds to a validated vehicle entry.
    """
    entry_log = models.ForeignKey(
        'terminal.EntryLog',   # ✅ Updated reference
        on_delete=models.CASCADE,
        related_name='trips',
        null=True,
        blank=True
    )

    departure_time = models.DateTimeField()
    status = models.CharField(max_length=50, default='Scheduled')

    def __str__(self):
        log_info = f" for {self.entry_log}" if self.entry_log else ""
        return f"Trip{log_info} at {self.departure_time.strftime('%Y-%m-%d %H:%M')}"
