from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True, blank=False)  # Ensure email is unique and cannot be blank
#     role = models.CharField(
#         max_length=10,
#         choices=[
#             ('admin', 'Admin'),
#             ('staff', 'Staff'),
#             ('user', 'User'),  # General users
#         ],
#         default='user'  # Default role is 'user'
#     )
#     bio = models.TextField(blank=True, null=True)  # Optional bio field
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Optional profile picture field

#     USERNAME_FIELD = 'email'  # Use email as the unique identifier
#     REQUIRED_FIELDS = ['username']  # Username is required for creating superusers

#     def __str__(self):
#         return self.email




class User(models.Model):
    username = models.CharField(max_length=255)
    email= models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=255)
    role=models.CharField(default='User')
    


class Item(models.Model):
    name = models.CharField(max_length=255) 
    description = models.CharField(max_length=255)  
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user') 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']