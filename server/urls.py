from django.urls import path
from .views import *

app_name = 'server'

urlpatterns = [
    path('home/', home, name='home'),
    path('home-men/', home_men, name='home-men'),
    path('home-kids/', home_kids, name='home-kids'),
    path('shop/', shop, name='shop-no-tag'),
    path('shop/<str:tag>/<str:sub_title>/', shop, name='shop'),
]
