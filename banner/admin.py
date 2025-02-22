from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin

# Women
@admin.register(WomenBanner)
class WomenBannerAdmin(ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(WomenCollection) 
class WomenCollectionAdmin(ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(WomenFeaturedProduct)
class WomenFeaturedProductAdmin(ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'sub_title')


@admin.register(WomenMidBanner)
class WomenMidBannerAdmin(ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)








# Men
@admin.register(MenBanner)
class MenBannerAdmin(ModelAdmin):
    list_display = ('id', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id',)

@admin.register(MenCollection) 
class MenCollectionAdmin(ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(MenFeaturedProduct)
class MenFeaturedProductAdmin(ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'sub_title')

@admin.register(MenMidBanner)
class MenMidBannerAdmin(ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(MenCountdown)
class MenCountdownAdmin(ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(MenBarText)
class MenBarTextAdmin(ModelAdmin):
    list_display = ('text', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text',)







# Kids
@admin.register(KidsBanner)
class KidsBannerAdmin(ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(KidsCollection) 
class KidsCollectionAdmin(ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(KidsMidBanner)
class KidsMidBannerAdmin(ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(KidBarText)
class KidBarTextAdmin(ModelAdmin):
    list_display = ('text', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text',)
