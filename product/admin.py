from django.contrib import admin
from .models import Product, ProductVariant, Category, SubCategory, Tag, ProductImage


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    list_filter = ('category', 'sub_category', 'tags')

admin.site.register(Category)
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_filter = ('category__name',)


admin.site.register(Tag)
admin.site.register(ProductImage)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    readonly_fields = ('sku',)
    list_display = ('sku', 'product', 'usual_price', 'discount_price', 'stock', 'returned_quantity', 'get_variant_name')
    list_filter = ('product','stock','returned_quantity', 'is_active')
    search_fields = ('product__name', 'sku')
    list_per_page = 20
