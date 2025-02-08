from django.urls import path
from .views import *

app_name = 'server'

urlpatterns = [
    path('home/', home, name='home'),
    path('shop/', shop, name='shop-no-tag'),
    path('shop/<str:tag>/<str:sub_title>/', shop, name='shop'),
]
