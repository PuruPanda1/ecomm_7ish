from django.db import models
from users.models import CustomUser
from product.models import ProductVariant

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email}"
    
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlist_items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wishlist.user.email} --> {self.product_variant.product.name}"

