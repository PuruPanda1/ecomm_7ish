from django.contrib import admin
from .models import Order, OrderItem, Returns

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('total_price_pre_tax', 'total_tax', 'total_price')
    
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ('total_price_pre_tax', 'total_tax', 'order_total')
    list_display = ('id', 'user', 'order_date', 'order_status', 'order_total')

class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ('total_price_pre_tax', 'total_tax', 'total_price')
    list_display = ('order', 'product_variant', 'quantity', 'total_price')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin) 
admin.site.register(Returns)