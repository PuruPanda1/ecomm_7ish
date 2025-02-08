from django.contrib import admin
from .models import Product, ProductVariant, Attribute, AttributeValue, Category, SubCategory, Tag

class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Tag)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    readonly_fields = ('sku',)
    list_display = ('sku', 'product', 'usual_price', 'discount_price', 'stock', 'returned_quantity', 'get_variant_name')
    list_filter = ('product','stock','returned_quantity', 'is_active')
    search_fields = ('product__name', 'sku')
    list_per_page = 20
