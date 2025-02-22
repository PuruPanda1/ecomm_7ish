from django.contrib import admin
from .models import Order, OrderItem, Returns
from unfold.admin import ModelAdmin, TabularInline

class OrderItemInline(TabularInline):
    model = OrderItem
    readonly_fields = ('total_price_pre_tax', 'total_tax', 'total_price')
    
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ('total_price_pre_tax', 'total_tax', 'order_total')
    list_display = ('id', 'user', 'order_date', 'order_status', 'order_total')
    list_filter = ('order_status',)
    search_fields = ('user__email', 'id')
    list_per_page = 20

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    readonly_fields = ('total_price_pre_tax', 'total_tax', 'total_price')
    list_display = ('order', 'product_variant', 'quantity', 'total_price')

@admin.register(Returns)
class ReturnsAdmin(ModelAdmin):
    list_display = ('order_item', 'order_item', 'return_date', 'return_status',)
    list_filter = ('return_status',)
    search_fields = ('order_item__order__user__email', 'order_item__product_variant__product__name')