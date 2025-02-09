from django.shortcuts import render
from product.models import Product, Tag, Category, SubCategory
from banner.models import WomenBanner, WomenCollection, WomenMidBanner, MenBanner, MenCountdown, MenMidBanner, MenCollection, MenBarText, KidsBanner, KidsCollection, KidsMidBanner
from reviews.models import Review
from collaboration.models import Collaboration
from django.http import JsonResponse

# home view for women
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

def home_men(request):
    tags = Tag.objects.filter(category__name='Men', is_active=True, on_top=True)    
    # Banners for the page 
    banners = MenBanner.objects.filter(is_active=True) 
    countdown,countdown2 = MenCountdown.objects.filter(is_active=True)[:2]
    firstC,secondC,thirdC,fourthC = MenCollection.objects.filter(is_active=True).order_by('-id')[:4]
    mid_banner = MenMidBanner.objects.filter(is_active=True).first()
    men_bar_texts = MenBarText.objects.filter(is_active=True)
    # Products
    best_seller = Product.objects.filter(is_active=True, tags__name='Best Seller')
    sale = Product.objects.filter(is_active=True, tags__name='Sale')
    new_arrivals = Product.objects.filter(is_active=True, tags__name='New Arrivals')
    jeans = Product.objects.filter(is_active=True, tags__name='Jeans')
    print(jeans.count())
    return render(request, 'server/home-men.html', {
        'tags': tags,
        'banners': banners,
        'countdown': countdown,
        'countdown2': countdown2,
        'firstC': firstC,
        'secondC': secondC,
        'thirdC': thirdC,
        'fourthC': fourthC,
        'mid_banner': mid_banner,
        'best_seller': best_seller,
        'sale': sale,
        'new_arrivals': new_arrivals,
        'jeans': jeans,
        'men_bar_texts': men_bar_texts
    })

def home_kids(request):
    tags = Tag.objects.filter(category__name='Kids', is_active=True, on_top=True)    
    banners = KidsBanner.objects.filter(is_active=True) 
    mid_banner = KidsMidBanner.objects.filter(is_active=True).first()
    sub_categories = SubCategory.objects.filter(category__name='Kids')
    collections = KidsCollection.objects.filter(is_active=True)
    favorites = Product.objects.filter(is_active=True, tags__name ='New Arrivals')
    reviews = Review.objects.filter(is_active=True)[:2]
    collaborations = Collaboration.objects.filter(is_active=True)
    return render(request, 'server/home-kids.html', {
        'tags': tags,
        'banners': banners,
        'mid_banner': mid_banner,
        'sub_categories': sub_categories,
        'collections': collections,
        'favorites': favorites,
        'reviews': reviews,
        'collaborations': collaborations
    })

# normal redirect without any category or tag   
def shop_no_tag(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'server/shop.html', {
        'title': 'New Arrivals',
        'sub_title': 'Shop through our latest selection of Fashion',
        'products': products
    })

# using category - (Men | Women | Kids) and subcategory - (T-shirt | Jeans | Shorts | etc) to show the products
def shop_category(request, category, subcategory):
    products = Product.objects.filter(category__name=category, sub_category__name=subcategory, is_active=True)
    return render(request, 'server/shop.html', {
        'title': subcategory,
        'sub_title': subcategory.description,
        'products': products
    })

# redirect from banners/ collections/ featured products to shop page with tag and sub_title
def shop_with_tag(request, category, tag, sub_title):
    if tag is None:
        tag = 'New Arrival'
    if sub_title is None:
        sub_title = 'Shop through our latest selection of Fashion'

    if tag is None:
        products = Product.objects.filter(category__name=category, is_active=True)
    else:
        products = Product.objects.filter(category__name=category, tags__name=tag, is_active=True)

    return render(request, 'server/shop.html', {
        'title': tag,
        'sub_title': sub_title,
        'products': products
    })