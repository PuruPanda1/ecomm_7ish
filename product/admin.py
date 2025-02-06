from django.contrib import admin
from .models import *

class ProductVariantImageInline(admin.TabularInline):
    model = ProductVariantImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand_name', 'description', 'category', 'sub_category')

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'usual_price', 'discount_price', 'stock', 'returned_quantity', 'get_variant_name')
    list_filter = ('product','stock','returned_quantity', 'is_active')
    search_fields = ('product__name', 'sku')
    list_per_page = 20
    filter_horizontal = ('attributes',)
    inlines = [ProductVariantImageInline]

admin.site.register(Category)
admin.site.register(SubCategory)