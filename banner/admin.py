from django.contrib import admin
from .models import WomenBanner, MenBanner, WomenCollection, MenCollection, WomenFeaturedProduct, MenFeaturedProduct, WomenMidBanner, MenMidBanner, MenCountdown

admin.site.register(WomenBanner)
admin.site.register(MenBanner)
admin.site.register(WomenCollection)
admin.site.register(MenCollection)
admin.site.register(WomenFeaturedProduct)
admin.site.register(MenFeaturedProduct)
admin.site.register(WomenMidBanner)
admin.site.register(MenMidBanner)
admin.site.register(MenCountdown)