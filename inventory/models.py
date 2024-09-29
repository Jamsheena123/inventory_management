from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)  # Ensure email is unique and cannot be blank
    role = models.CharField(
        max_length=10,
        choices=[
            ('admin', 'Admin'),
            ('staff', 'Staff'),
            ('user', 'User'),  # General users
        ],
        default='user'  # Default role is 'user'
    )
    bio = models.TextField(blank=True, null=True)  # Optional bio field
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Optional profile picture field

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['username']  # Username is required for creating superusers

    def __str__(self):
        return self.email


class Item(models.Model):
    name = models.CharField(max_length=255)  # Name of the inventory item
    description = models.TextField(blank=True, null=True)  # Optional description of the item
    quantity = models.PositiveIntegerField(default=0)  # Quantity of the item in stock
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the item
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')  # The user who added the item
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the item was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the item was last updated

    def __str__(self):
        return f"{self.name} - {self.quantity} in stock"

    class Meta:
        ordering = ['-created_at']