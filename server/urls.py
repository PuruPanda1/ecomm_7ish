from django.urls import path
from .views import home

app_name = 'server'

urlpatterns = [
    path('home/', home, name='home'),
]
