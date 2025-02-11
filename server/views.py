from django.shortcuts import render
from product.models import Product, Tag, Category, SubCategory
from banner.models import WomenBanner, WomenCollection, WomenMidBanner, MenBanner, MenCountdown, MenMidBanner, MenCollection, MenBarText, KidsBanner, KidsCollection, KidsMidBanner, KidBarText
from reviews.models import Review
from collaboration.models import Collaboration
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.db import models
# home view for women
def home_women(request):
    # header tags
    men_tags =  Tag.objects.filter(category__name='Men', is_active=True)    
    women_tags =  Tag.objects.filter(category__name='Women', is_active=True)    
    kids_tags =  Tag.objects.filter(category__name='Kids', is_active=True)    
    header_products = Product.objects.filter(is_active=True, tags__name='Best Seller')[:2]
    current_tab = 'Women'
    # specific page context
    tags = Tag.objects.filter(category__name='Women', is_active=True, on_top=True)    
    banners = WomenBanner.objects.filter(is_active=True) 
    mid_banner = WomenMidBanner.objects.filter(is_active=True).first()
    sub_categories = SubCategory.objects.filter(category__name='Women')
    collections = WomenCollection.objects.filter(is_active=True)
    favorites = Product.objects.filter(is_active=True, tags__name ='New Arrivals', category__name='Women')
    reviews = Review.objects.filter(is_active=True)[:2]
    collaborations = Collaboration.objects.filter(is_active=True)
    return render(request, 'server/home-women.html', {
        'tags': tags,
        'banners': banners,
        'mid_banner': mid_banner,
        'sub_categories': sub_categories,
        'collections': collections,
        'favorites': favorites,
        'reviews': reviews,
        'collaborations': collaborations,
        'men_tags': men_tags,
        'women_tags': women_tags,
        'kids_tags': kids_tags,
        'header_products': header_products,
        'current_tab': current_tab
    })

def home_men(request):
    # header tags
    men_tags =  Tag.objects.filter(category__name='Men', is_active=True)    
    women_tags =  Tag.objects.filter(category__name='Women', is_active=True)    
    kids_tags =  Tag.objects.filter(category__name='Kids', is_active=True) 
    header_products = Product.objects.filter(is_active=True, tags__name='Best Seller')[:2]
    current_tab = 'Men'
    # specific page context
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
        'men_bar_texts': men_bar_texts,
        'men_tags': men_tags,
        'women_tags': women_tags,
        'kids_tags': kids_tags,
        'header_products': header_products,
        'current_tab': current_tab
    })

def home_kids(request):
    # header tags
    men_tags =  Tag.objects.filter(category__name='Men', is_active=True)    
    women_tags =  Tag.objects.filter(category__name='Women', is_active=True)    
    kids_tags =  Tag.objects.filter(category__name='Kids', is_active=True)
    header_products = Product.objects.filter(is_active=True, tags__name='Best Seller')[:2]
    current_tab = 'Kids'
    # specific page context
    banners =KidsBanner.objects.filter(is_active=True)
    flash_sale_products = Product.objects.filter(is_active=True, tags__name='Flash Sale')
    collections = KidsCollection.objects.filter(is_active=True)
    favorites = Product.objects.filter(is_active=True, tags__name='Favorites')
    mid_banner = KidsMidBanner.objects.filter(is_active=True).first()
    kid_bar_texts = KidBarText.objects.filter(is_active=True)
    return render(request, 'server/home-kids.html', {
        'banners': banners,
        'flash_sale_products': flash_sale_products,
        'collections': collections,
        'favorites': favorites,
        'mid_banner': mid_banner,
        'kid_bar_texts': kid_bar_texts,
        'men_tags': men_tags,
        'women_tags': women_tags,
        'kids_tags': kids_tags,
        'header_products': header_products,
        "current_tab": current_tab
    })

# normal redirect without any category or tag   
def shop(request):
    categories = Category.objects.filter()
    selected_category = Category.objects.get(id=1)
    sub_categories = SubCategory.objects.filter(category=selected_category)
    # TODO Implement infinite scroll using pagination
    products = Product.objects.filter(is_active=True)[:1]
    sale_products = Product.objects.filter(is_active=True, tags__name__iexact='Sale')
    return render(request, 'server/shop.html', {
        'title': 'New Arrivals',
        'products': products,
        'categories': categories,
        'sub_categories': sub_categories,
        'selected_category': selected_category,
        'sale_products': sale_products
    })

# using category - (Men | Women | Kids) and subcategory - (T-shirt | Jeans | Shorts | etc) to show the products
def shop_category(request, category, subcategory):
    if subcategory == 'none':
        products = Product.objects.filter(category__name=category, is_active=True)
    else:
        products = Product.objects.filter(category__name=category, sub_category__name=subcategory, is_active=True)
        categories = Category.objects.filter()
        sub_categories = SubCategory.objects.filter(category__name='Women')
        selected_category = 'Women'
    return render(request, 'server/shop.html', {
        'title': subcategory,
        'products': products,
        'categories': categories,
        'sub_categories': sub_categories,
        'selected_category': selected_category
    })

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    # TODO Implement product detail view
    return render(request, 'server/product-detail.html', {
        'product': product
    })


# partials views

def update_category(request, category_id):
    if not request.headers.get('HX-Request'):
        return HttpResponseBadRequest("HTMX request required")
        
    try:
        categories = Category.objects.all()
        selected_category = Category.objects.get(id=category_id)
        sub_categories = SubCategory.objects.filter(category=selected_category)
        products = Product.objects.filter(category=selected_category, is_active=True)
        
        return render(request, 'server/partials/update-categories.html', {
            'products': products,
            'categories': categories,
            'selected_category': selected_category,
            'sub_categories' : sub_categories
        })
    except Category.DoesNotExist:
        return HttpResponseNotFound("Category not found")
    
def update_sub_category(request, category, sub_category_id):
    if not request.headers.get('HX-Request'):
        return HttpResponseBadRequest("HTMX request required")
        
    try:
        print("Inside try block")
        selected_category = Category.objects.get(name=category)
        print(selected_category.id, 'and ', selected_category.name)
        sub_categories = SubCategory.objects.filter(category=selected_category)
        selected_sub_category = SubCategory.objects.get(id=sub_category_id)
        products = Product.objects.filter(category=selected_category, sub_category=selected_sub_category, is_active=True)
        
        return render(request, 'server/partials/update-sub-categories.html', {
            'products': products,
            'selected_category': selected_category,
            'sub_categories': sub_categories,
            'selected_sub_category': selected_sub_category,
        })
    except Category.DoesNotExist:
        return HttpResponseNotFound("Category not found")

def update_sort(request, sort_by):
    if not request.headers.get('HX-Request'):
        return HttpResponseBadRequest("HTMX request required")
    
    products = Product.objects.filter(is_active=True)
    if sort_by == 'featured':
        products = products.order_by('-id')
    elif sort_by == 'a-z':
        products = products.order_by('name')
    elif sort_by == 'z-a':
        products = products.order_by('-name')
    elif sort_by == 'price-low-high':
        products = products.annotate(min_price=models.Min('variants__discount_price')).order_by('min_price')
    elif sort_by == 'price-high-low':
        products = products.annotate(min_price=models.Min('variants__discount_price')).order_by('-min_price')
    elif sort_by == 'date-old-new':
        products = products.order_by('created_at')
    elif sort_by == 'date-new-old':
        products = products.order_by('-created_at')
    
    return render(request, 'server/partials/product-grid.html', {
        'products': products
    })

# filter views

def filter_products_by_sub_category(request, category_id):
    selected_category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=selected_category)

    # Get selected subcategories
    selected_sub_categories = request.GET.getlist("sub_category")

    if selected_sub_categories:
        products = products.filter(sub_category__id__in=selected_sub_categories)

    return render(request, "server/partials/product-grid.html", {"products": products})