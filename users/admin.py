from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from unfold.admin import ModelAdmin

@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    model = CustomUser
    list_display = ['email', 'phone_number', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name' ,'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

@admin.register(UserAddress)
class UserAddressAdmin(ModelAdmin):
    model = UserAddress
    list_display = ['user', 'name', 'street_address', 'city', 'state', 'postal_code', 'country', 'mobile_number', 'address_nickname', 'email']
    list_filter = ['user', 'name', 'country', 'state', 'city' ,'address_nickname']
    fieldsets = (
        (None, {'fields': ('user', 'name')}),
        ('Address', {'fields': ('street_address', 'city', 'state', 'postal_code', 'country', 'mobile_number', 'address_nickname', 'email')}),
    )
    search_fields = ('user__email', 'name')
    ordering = ('user__email', 'name')