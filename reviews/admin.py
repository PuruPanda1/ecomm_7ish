from django.contrib import admin
from .models import Review
from unfold.admin import ModelAdmin

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'product', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'product')
    search_fields = ('title', 'review')

