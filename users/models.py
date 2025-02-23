from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=100, blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  # Use the custom manager

    def __str__(self):
        return self.email

class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100)  # e.g. 'home', 'work', etc
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20, default='')
    address_nickname = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    
    class Meta:
        unique_together = ['user', 'name']  # Ensures name uniqueness per user
        
    def __str__(self):
        return f"{self.user.email} - {self.name}"