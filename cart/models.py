from django.db import models
from users.models import CustomUser
from product.models import ProductVariant


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    @property
    def total_price_pre_tax(self):
        return sum(item.total_price_pre_tax for item in self.cart_items.all())
    
    @property
    def free_shipping_remaining(self):
        return 999 - self.total_price_pre_tax
    
    @property 
    def total_tax(self):
        return sum(item.total_tax for item in self.cart_items.all())
        
    @property
    def cart_total(self):
        return self.total_price_pre_tax + self.total_tax
    
    def __str__(self):
        return f"{self.user.email}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

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
        return f"{self.cart.user.email} --> {self.product_variant.product.name}"

    @classmethod
    def create_cart_item(cls, cart: Cart, product_variant: ProductVariant, quantity: int):
        cart_item = cls(
            cart=cart,
            product_variant=product_variant,
            quantity=quantity,
        )
        cart_item.save()
        return cart_item
    
    def save(self, *args, **kwargs):
        if self.quantity > self.product_variant.stock:
            raise ValueError(f"Error: Out of stock. Available stock: {self.product_variant.stock}")
        super().save(*args, **kwargs)