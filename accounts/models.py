from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('driver', 'Driver'),
        ('admin', 'Admin'),
        ('staff_admin', 'Staff Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Add related_name to the inherited fields to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Unique related_name
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Unique related_name
        related_query_name='custom_user'
    )
    
    def __str__(self):
        return self.username