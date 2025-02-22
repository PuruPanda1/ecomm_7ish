from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin, TabularInline

class CartItemInline(TabularInline):
    model = CartItem
    readonly_fields = ('total_price_pre_tax', 'total_tax', 'total_price')

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    inlines = [CartItemInline]
    readonly_fields = ('total_price_pre_tax', 'total_tax', 'cart_total')

@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    model = CartItem
    readonly_fields = ('total_price_pre_tax', 'total_tax', 'total_price')
