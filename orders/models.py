from django.db import models
from users.models import CustomUser, UserAddress
from product.models import ProductVariant
from decimal import Decimal

# total_pre_tax = total_price + shipping_cost
# total_tax = total_pre_tax * tax_rate
# order_total = total_pre_tax + total_tax
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('confirmed', 'Confirmed'), 
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
        ('refunded', 'Refunded'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='ordered')
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='shipping_address')
    billing_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='billing_address')
    @property
    def total_price_pre_tax(self):
        return sum(item.total_price_pre_tax for item in self.order_items.all())
    
    @property 
    def total_tax(self):
        return sum(item.total_tax for item in self.order_items.all())
        
    @property
    def order_total(self):
        return self.total_price_pre_tax + self.total_tax + self.shipping_cost
    
    def __str__(self):
        return f"Order {self.id} - {self.user.email}"
    
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    @property
    def price(self):
        return self.product_variant.discount_price
    @property
    def total_price_pre_tax(self):
        return self.quantity * self.price
    @property
    def tax_rate(self):
        return self.product_variant.product.tax_rate
    @property
    def total_tax(self):
        return self.total_price_pre_tax * self.tax_rate
    @property
    def total_price(self):
        return self.total_price_pre_tax + self.total_tax

    def __str__(self):
        return f"{self.quantity} x {self.product_variant.product.name} in Order {self.order.id}"
    
    
    @classmethod
    def create_order_item(cls, order: Order, product_variant: ProductVariant, quantity: int):
        order_item = cls(
            order=order,
            product_variant=product_variant,
            quantity=quantity,
        )
        order_item.save()
        return order_item
    
    def save(self, *args, **kwargs):
        if self.quantity > self.product_variant.stock:
            raise ValueError(f"Error: Out of stock. Available stock: {self.product_variant.stock}")
        # Reduce stock when saving an order item
        self.product_variant.stock -= self.quantity
        self.product_variant.save()
        super().save(*args, **kwargs)

class Returns(models.Model):
    RETURN_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='returns')
    return_date = models.DateTimeField(auto_now_add=True)
    return_reason = models.TextField()
    return_images = models.ImageField(upload_to='returns/')
    return_status = models.CharField(max_length=100, choices=RETURN_STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if self.return_status == 'pending':
            self.order_item.order.order_status = 'returned'
            self.order_item.order.save()
        elif self.return_status == 'approved':
            self.order_item.order.order_status = 'refunded'
            self.order_item.order.save()
            self.order_item.order.payment.payment_status = 'refunded'
            self.order_item.order.payment.save()
            self.order_item.product_variant.returned_quantity += self.order_item.quantity
            self.order_item.product_variant.save()
        elif self.return_status == 'rejected':
            self.order_item.order.order_status = 'delivered'
            self.order_item.order.save()
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return f"Return {self.id} - {self.order_item.product_variant.product.name}"
    
    