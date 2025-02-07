from django.contrib import admin
from .models import *


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    readonly_fields = ('added_at',)
    
class WishlistAdmin(admin.ModelAdmin):
    inlines = [WishlistItemInline]

admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem)