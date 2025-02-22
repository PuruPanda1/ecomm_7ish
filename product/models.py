from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from smart_selects.db_fields import ChainedForeignKey

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sub_categories/', default='sub_categories/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tags', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='tags/', default='tags/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    on_top = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    description = models.TextField()
    features = models.TextField(help_text="Enter each feature on a new line.", default='')
    materials_care = models.TextField(help_text="Enter each material/care instruction on a new line.", default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = ChainedForeignKey(SubCategory, chained_field="category", chained_model_field="category", show_all=False, auto_choose=True, sort=True) 
    # tags = GroupedForeignKey(Tag, "category") 
    # sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tag', default=None)
    tax_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def get_features_list(self):
        return [feature.strip() for feature in self.features.split("\n") if feature.strip()]

    def get_materials_care_list(self):
        return [material.strip() for material in self.materials_care.split("\n") if material.strip()]




class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    usual_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    returned_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Attributes
    color = models.CharField(max_length=255, default='dark')
    size = models.CharField(max_length=128, default='M')

    @property
    def sku(self):
        return self.get_variant_name()

    @property
    def discount_percentage(self):
        """Calculate and return the discount percentage."""
        if self.discount_price and self.usual_price and self.usual_price > self.discount_price:
            return round(((self.usual_price - self.discount_price) / self.usual_price) * 100)
        return 0  

    def __str__(self):
        return f"{self.product.name} --> {self.sku}"

    def get_variant_name(self):
        return f"{self.product.name} - {self.color} - {self.size}"
    
    def get_color(self):
        return self.color

    def get_images(self):
        color = self.get_color()
        if color:
            return self.product.images.filter(color__iexact=color)
        else:
            return self.product.images.filter(color__isnull=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    color = models.CharField(max_length=255, default='dark')
    image = models.ImageField(upload_to='products/')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.color}"
    

# Sale timmer

class Sale(models.Model):
    product = models.ManyToManyField(Product, related_name='sale')
    sale_name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def time_left(self):
        """Calculate and return the time remaining until end_date in seconds"""
        now = timezone.now()
        if now > self.end_date:
            return 0
        time_diff = self.end_date - now
        return int(time_diff.total_seconds())
    
    def __str__(self):
        return f"{self.sale_name} - {self.start_date} to {self.end_date}"
    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=255)
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.coupon_code} - {self.discount_percentage}"
    
    