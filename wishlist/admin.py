from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin, TabularInline


class WishlistItemInline(TabularInline):
    model = WishlistItem
    readonly_fields = ('added_at',)
    
@admin.register(Wishlist)
class WishlistAdmin(ModelAdmin):
    inlines = [WishlistItemInline]

@admin.register(WishlistItem)
class WishlistItemAdmin(ModelAdmin):
    list_display = ('wishlist', 'product','added_at')
    list_filter = ('wishlist', 'product')
    search_fields = ('wishlist__user__email', 'product__name')