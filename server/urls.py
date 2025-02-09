from django.urls import path
from .views import *

app_name = 'server'

urlpatterns = [
    path('home/', home, name='home'),
    path('home-men/', home_men, name='home-men'),
    path('home-kids/', home_kids, name='home-kids'),
    path('shop/', shop_no_tag, name='shop-no-tag'),
    path('shop-category/<str:category>/<str:subcategory>/', shop_category, name='shop-category'), 
    path('shop-with-tag/<str:category>/<str:tag>/<str:sub_title>/', shop_with_tag, name='shop-with-tag'),
]
