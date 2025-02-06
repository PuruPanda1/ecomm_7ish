from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    tax_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Color", "Size"

    def __str__(self):
        return self.name

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)  # e.g., "Red", "Small"

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=50, unique=True)  # Stock Keeping Unit
    usual_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    returned_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Many-to-many relationship with AttributeValue
    attributes = models.ManyToManyField(AttributeValue)

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

    def get_variant_name(self):
        return ", ".join([str(attr) for attr in self.attributes.all()])

class ProductVariantImage(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    

    def __str__(self):
        return f"{self.product_variant.product.name} - {self.product_variant.created_at}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/')
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
