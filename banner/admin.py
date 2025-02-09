from django.contrib import admin
from .models import *

# Women
admin.site.register(WomenBanner)
admin.site.register(WomenCollection)
admin.site.register(WomenFeaturedProduct)
admin.site.register(WomenMidBanner)

# Men
admin.site.register(MenBanner)
admin.site.register(MenCollection)
admin.site.register(MenFeaturedProduct)
admin.site.register(MenMidBanner)
admin.site.register(MenCountdown)
admin.site.register(MenBarText)