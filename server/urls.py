from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

# app_name = 'server'

urlpatterns = [
    # authentication
     path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="server/users/password-reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="server/users/password-reset-mail-sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="server/users/password-reset-confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="server/users/password_reset_complete.html"), name="password_reset_complete"),

    # my account
    path('my-account/', my_account, name='my-account'),
    path('account_action/<str:option>/', account_action, name='account-action'),
    path('order-detail/<int:order_id>/', order_detail, name='order-detail'),

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

    # wishlist url
    path('wishlist/', wishlist_page, name='wishlist'),
    path('add-remove-wishlist-item/<int:product_id>/', add_remove_wishlist_item, name='add-remove-wishlist-item'),
    path('add-remove-wishlist-item_product_page/<int:product_id>/', add_remove_wishlist_item_product_page, name='add-remove-wishlist-item-product-page'),
    path('remove-item-from-wishlist/<int:product_id>/', remove_item_from_wishlist, name='remove-item-from-wishlist'),

    # cart urls
    path('cart/', cart_page, name='cart'),
    path('remove-cart-item/<int:product_varaint_id>/', remove_cart_item, name='remove-cart-item'),
    path('cart-update-quantity/<int:product_varaint_id>/<str:option>/', cart_update_quantity, name='cart-update-quantity'),

    # sidebar cart urls
    path('update-cart-count/', update_cart_count, name='update-cart-count'),
    path('update-cart-sub-total/', update_cart_sub_total, name='update-cart-sub-total'),
    path('add-cart-item/<int:product_id>/<int:quantity>', add_cart_item, name='add-cart-item'),
    path('remove-sidebar-cart-item/<int:product_varaint_id>/', remove_sidebar_cart_item, name='remove-sidebar-cart-item'),

    # checkout urls
    path('checkout/', checkout_page, name='checkout'),
    path('add-address/', add_address, name='add-address'),     
    path('apply-coupon-code/<int:gift_wrap>/', apply_coupon_code, name='apply-coupon-code'),
    
    # orders urls
    path('create-order/<int:need_gift_wrap>/<str:order_note>/', create_order, name='create-order'),
    path('order-success/', order_success, name='order-success'),
    path('order-failure/', order_failure, name='order-failure'),
]
