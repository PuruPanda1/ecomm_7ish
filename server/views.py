from django.shortcuts import render
from product.models import Product, Tag, Category, SubCategory
from banner.models import WomenBanner, WomenCollection, WomenMidBanner
from reviews.models import Review
from collaboration.models import Collaboration

def home(request):
    tags = Tag.objects.filter(category__name='Women', is_active=True, on_top=True)    
    banners = WomenBanner.objects.filter(is_active=True) 
    mid_banner = WomenMidBanner.objects.filter(is_active=True).first()
    sub_categories = SubCategory.objects.filter(category__name='Women')
    collections = WomenCollection.objects.filter(is_active=True)
    favorites = Product.objects.filter(is_active=True, tags__name ='New Arrivals')
    reviews = Review.objects.filter(is_active=True)[:2]
    collaborations = Collaboration.objects.filter(is_active=True)
    return render(request, 'server/home.html', {
        'tags': tags,
        'banners': banners,
        'mid_banner': mid_banner,
        'sub_categories': sub_categories,
        'collections': collections,
        'favorites': favorites,
        'reviews': reviews,
        'collaborations': collaborations
    })

# using tag to show the banner of the shops page and sub_title to show the sub_title of the shops page
def shop(request, tag=None, sub_title=None):
    if tag is None:
        tag = 'New Arrival'
    if sub_title is None:
        sub_title = 'Shop through our latest selection of Fashion'

    if tag is None:
        products = Product.objects.filter(is_active=True)
    else:
        products = Product.objects.filter(tags__name=tag, is_active=True)
        
    return render(request, 'server/shop.html', {
        'title': tag,
        'sub_title': sub_title,
        'products': products
    })