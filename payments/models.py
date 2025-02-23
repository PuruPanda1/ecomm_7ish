from django.db import models
from orders.models import Order

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('processing', 'Processing'),
        ('refunded', 'Refunded'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
        ('cod', 'Cash on Delivery'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_method_details = models.TextField(default='NA') # will contain upi id or card details -- NA if cod
    transaction_id = models.CharField(max_length=100, default='NA') # NA if cod
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS_CHOICES, default='processing')
    
    @property
    def amount(self):
        return self.order.order_total
    
    def __str__(self):
        return f"Payment {self.id} - {self.order.user.email} --> {self.order.id}"
    