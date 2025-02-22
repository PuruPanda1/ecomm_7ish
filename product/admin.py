from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin, TabularInline


class ProductVariantInline(TabularInline):
    model = ProductVariant
    extra = 1

class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1  # Allows adding multiple images per product
    ordering = ['order'] 

@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    list_display = ('product', 'color', 'image', 'order')
    list_filter = ('product', 'color')
    ordering = ('order',)
    
@admin.register(Product)
class ProductAdmin(ModelAdmin):
    inlines = [ProductVariantInline, ProductImageInline]
    list_filter = ('category', 'sub_category', 'tags')
    list_display = ('name', 'brand_name', 'created_at', 'updated_at', 'is_active')
    search_fields = ('name', 'brand_name',)

    class Media:
        js = [
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js',
            'smart-selects/admin/js/chainedfk.js',
            'smart-selects/admin/js/bindfields.js',
        ]

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_filter = ('name',)
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(SubCategory)
class SubCategoryAdmin(ModelAdmin):
    list_filter = ('category__name',)


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('category__name',)


@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    readonly_fields = ('sku',)
    list_display = ('sku', 'product', 'usual_price', 'discount_price', 'stock', 'returned_quantity', 'get_variant_name')
    list_filter = ('is_active', 'product','stock','returned_quantity', 'size', 'color')
    search_fields = ('product__name', 'sku')
    list_per_page = 20


# Sale and Coupon Admin

@admin.register(Sale)
class SaleAdmin(ModelAdmin):
    list_display = ('sale_name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('sale_name',)

@admin.register(Coupon)
class CouponAdmin(ModelAdmin):
    list_display = ('coupon_code', 'discount_percentage', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('coupon_code',)