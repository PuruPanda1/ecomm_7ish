from django.urls import path
from .views import *

app_name = 'server'

urlpatterns = [
    path('', home_women, name='home-women'),
    path('home/men/', home_men, name='home-men'),
    path('home/kids/', home_kids, name='home-kids'),
    path('shop/', shop, name='shop'), # for direct shop page without tag
    path('shop-category/<str:category>/<str:subcategory>/', shop_category, name='shop-category'), # shop through tags/ featured category
    path('product-detail/<int:product_id>/', product_detail, name='product-detail'),

    # partials url
    path('update-category/<int:category_id>/', update_category, name='update-category'),
    path('update-sort/<str:sort_by>/', update_sort, name='update-sort'),
    path('filter-products/<int:category_id>/', filter_products, name='filter-products'),

    # product detail url
    path('product-varaint-detail/<int:product_id>/', product_varaint_detail, name='product-varaint-detail'),
    path('update-quantity/<int:product_variant_id>/<str:option>/<int:quantity>/', update_quantity, name='update-quantity'),
    path('sort-reviews/<int:product_id>/<str:sort_by>/', sort_reviews, name='sort-reviews'),
    path('submit-review/<int:product_id>/', submit_review, name='submit-review'),

]
