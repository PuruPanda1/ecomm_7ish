from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_date', 'payment_method', 'payment_status', 'amount')
    readonly_fields = ('amount',)
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('order__user__email', 'transaction_id')
    list_per_page = 20
