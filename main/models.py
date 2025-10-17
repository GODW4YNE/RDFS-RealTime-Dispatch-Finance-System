from django.db import models
from terminal.models import Queue

# Create your models here.
class Trip(models.Model):
    queue_entry = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name='trips', null=True, blank=True)
    departure_time = models.DateTimeField()
    status = models.CharField(max_length=50, default='Scheduled')
    
    def __str__(self):
        return f"Trip at {self.departure_time}"