from django.urls import path
from .views import *

app_name = 'server'

urlpatterns = [
    path('home/women/', home_women, name='home-women'),
    path('home/men/', home_men, name='home-men'),
    path('home/kids/', home_kids, name='home-kids'),
    path('shop/', shop, name='shop'), # for direct shop page without tag
    path('shop-category/<str:category>/<str:subcategory>/', shop_category, name='shop-category'), # shop through tags/ featured category
    path('product-detail/<int:product_id>/', product_detail, name='product-detail'),

    # partials url
    path('update-category/<int:category_id>/', update_category, name='update-category'),
    path('update-sort/<str:sort_by>/', update_sort, name='update-sort'),
    path('update-sub-category/<str:category>/<int:sub_category_id>/', update_sub_category, name='update-sub-category'),
]
