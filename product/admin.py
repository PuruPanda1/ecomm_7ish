from django.contrib import admin
from .models import *


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Allows adding multiple images per product
    ordering = ['order'] 

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'image', 'order')
    list_filter = ('product', 'color')
    ordering = ('order',)
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline, ProductImageInline]
    list_filter = ('category', 'sub_category', 'tags')

admin.site.register(Category)
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_filter = ('category__name',)


admin.site.register(Tag)



@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    readonly_fields = ('sku',)
    list_display = ('sku', 'product', 'usual_price', 'discount_price', 'stock', 'returned_quantity', 'get_variant_name')
    list_filter = ('product','stock','returned_quantity', 'is_active')
    search_fields = ('product__name', 'sku')
    list_per_page = 20


# Sale and Coupon Admin

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('sale_name',)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_code', 'discount_percentage', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('coupon_code',)