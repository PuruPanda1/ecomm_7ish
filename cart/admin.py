from django.contrib import admin
from .models import *

class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ('total_price_pre_tax', 'total_tax', 'total_price')

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    readonly_fields = ('total_price_pre_tax', 'total_tax', 'cart_total')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
