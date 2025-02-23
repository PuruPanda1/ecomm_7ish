from django.shortcuts import render, redirect
from users.models import UserAddress
from wishlist.models import Wishlist, WishlistItem
from cart.models import Cart, CartItem
from product.models import Product, Tag, Category, SubCategory, Sale, ProductVariant, Coupon
from banner.models import WomenBanner, WomenCollection, WomenMidBanner, MenBanner, MenCountdown, MenMidBanner, MenCollection, MenBarText, KidsBanner, KidsCollection, KidsMidBanner, KidBarText
from reviews.models import Review
from collaboration.models import Collaboration
from orders.models import Order, OrderItem
from django.utils import timezone
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.db import models
import time
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import math
from decimal import Decimal
from django.contrib.auth import get_user_model
from .utils import calculate_cart_total, calculate_discount
from django.db import transaction

User = get_user_model()

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home-women") 
    
    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "server/users/signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return render(request, "server/users/signup.html")

        # Create new user
        user = User.objects.create_user(email=email, password=password1)
        user.save()

        login(request, user)  # Log in the new user
        return redirect("home-women")

    return render(request, "server/users/signup.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home-women") 
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home-women")  # Redirect to your dashboard or home page
        else:
            messages.error(request, "Invalid email or password")  # Display error message

    return render(request, "server/users/login.html") 

def logout_view(request):
    logout(request)
    return redirect("login")

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
    best_seller = Product.objects.filter(is_active=True,category__name='Men', tags__name__iexact='Best Seller')
    sale = Product.objects.filter(is_active=True,category__name='Men', tags__name__iexact='Sale')
    new_arrivals = Product.objects.filter(is_active=True,category__name='Men', tags__name__iexact='New Arrivals')
    jeans = Product.objects.filter(is_active=True,category__name='Men', tags__name__iexact='Jeans')
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
    # header tags
    men_tags =  Tag.objects.filter(category__name='Men', is_active=True)    
    women_tags =  Tag.objects.filter(category__name='Women', is_active=True)    
    kids_tags =  Tag.objects.filter(category__name='Kids', is_active=True)    
    header_products = Product.objects.filter(is_active=True, tags__name='Best Seller')[:2]
    current_tab = ''
    # specific page context
    categories = Category.objects.filter()
    selected_category = Category.objects.get(id=1)
    sub_categories = SubCategory.objects.filter(category=selected_category)
    # TODO Implement infinite scroll using pagination
    products = Product.objects.filter(is_active=True, category=selected_category)
    sale_products = Product.objects.filter(is_active=True, tags__name__iexact='Sale')
    
    prices = [variant.discount_price for product in products for variant in product.variants.all()]
    min_price = min(prices)
    max_price = max(prices)

    # filter form
    brands = products.values_list('brand_name', flat=True).distinct()
    sizes = products.values_list('variants__size', flat=True).distinct()
    colors = products.values_list('variants__color', flat=True).distinct()

    return render(request, 'server/shop.html', {
        'men_tags': men_tags,
        'women_tags': women_tags,
        'kids_tags': kids_tags,
        'header_products': header_products,
        'current_tab': current_tab,
        'title': 'New Arrivals',
        'products': products,
        'categories': categories,
        'sub_categories': sub_categories,
        'selected_category': selected_category,
        'sale_products': sale_products,
        'sizes': sizes,
        'brands': brands,
        'min_price': min_price,
        'max_price': max_price,
        'colors': colors
    })

# using category - (Men | Women | Kids) and subcategory - (T-shirt | Jeans | Shorts | etc) to show the products
def shop_category(request, category, subcategory):
    # header tags
    men_tags =  Tag.objects.filter(category__name='Men', is_active=True)    
    women_tags =  Tag.objects.filter(category__name='Women', is_active=True)    
    kids_tags =  Tag.objects.filter(category__name='Kids', is_active=True)    
    header_products = Product.objects.filter(is_active=True, tags__name='Best Seller')[:2]
    current_tab = ''
    if subcategory == 'none':
        selected_category = Category.objects.get(name=category)
        products = Product.objects.filter(category=selected_category, is_active=True)
    else:
        selected_category = Category.objects.get(name=category)
        products = Product.objects.filter(category=selected_category, sub_category__name=subcategory, is_active=True)
        if products.count() == 0:
            products = Product.objects.filter(category=selected_category, tags__name=subcategory, is_active=True)
        categories = Category.objects.filter()
        sub_categories = SubCategory.objects.filter(category__name=category)
    return render(request, 'server/shop.html', {
        'men_tags': men_tags,
        'women_tags': women_tags,
        'kids_tags': kids_tags,
        'header_products': header_products,
        'current_tab': current_tab,
        'title': subcategory,
        'products': products,
        'categories': categories,
        'sub_categories': sub_categories,
        'selected_category': selected_category
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
        sizes = products.values_list('variants__size', flat=True).distinct()
        colors = products.values_list('variants__color', flat=True).distinct()
        brands = products.values_list('brand_name', flat=True).distinct()


        prices = [variant.discount_price for product in products for variant in product.variants.all()]
        min_price = min(prices)
        max_price = max(prices)

        
        return render(request, 'server/partials/update-categories.html', {
            'products': products,
            'categories': categories,
            'selected_category': selected_category,
            'sub_categories' : sub_categories,
            'sizes': sizes,
            'colors': colors,
            'brands': brands,
            'min_price': min_price,
            'max_price': max_price
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

def filter_products(request, category_id):
    
    selected_category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=selected_category)

    # Get selected subcategories
    selected_sub_categories = request.GET.getlist("sub_category")
    selected_brands = request.GET.getlist("brand")
    selected_sizes = request.GET.getlist("size")
    max_price = request.GET.get("max_price")
    min_price = request.GET.get("min_price")


    if selected_sub_categories:
        products = products.filter(sub_category__id__in=selected_sub_categories)

    if selected_brands:
        products = products.filter(brand_name__in=selected_brands)

    if selected_sizes:
        products = products.filter(variants__size__in=selected_sizes)

    if max_price:
        products = products.filter(variants__discount_price__lte=max_price).distinct()

    return render(request, "server/partials/update-filter-form.html", 
                  {"products": products,
                   "min_price": min_price,
                   "max_price": max_price,
                   "selected_category": selected_category
                    })


def product_detail(request, product_id):
    # header tags
    men_tags =  Tag.objects.filter(category__name='Men', is_active=True)    
    women_tags =  Tag.objects.filter(category__name='Women', is_active=True)    
    kids_tags =  Tag.objects.filter(category__name='Kids', is_active=True)    
    header_products = Product.objects.filter(is_active=True, tags__name='Best Seller')[:2]
    current_tab = ''
    # specific page context
    product = Product.objects.get(id=product_id)
    product_variant = product.variants.first()
    sizes = product.variants.values_list('size', flat=True).distinct()
    colors = product.variants.values_list('color', flat=True).distinct()
    selected_size = sizes.first()
    selected_color = colors.first()
    images = product.images.filter(color__iexact=selected_color)
    people_also_bought = Product.objects.filter(is_active=True, tags__name='Best Seller')[:5]
    reviews = Review.objects.filter(product=product, is_active=True).order_by('-created_at')
    return render(request, 'server/product-detail.html', {
        'men_tags': men_tags,
        'women_tags': women_tags,
        'kids_tags': kids_tags,
        'header_products': header_products,
        'current_tab': current_tab,
        'product': product,
        'product_variant': product_variant,
        'sizes': sizes,
        'colors': colors,
        'selected_size': selected_size,
        'selected_color': selected_color,
        'people_also_bought': people_also_bought,
        'images': images,
        'reviews': reviews
    })



def product_varaint_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    selected_size = request.GET.get('size')
    selected_color = request.GET.get('color')

    default_color = request.GET.get('selected_color')
    default_size = request.GET.get('selected_size')

    variant_color = selected_color or default_color
    variant_size = selected_size or default_size
    
    # default variant and images
    product_variant = product.variants.filter(color__iexact=variant_color, size__iexact=variant_size).first()
    images = product.images.filter(color__iexact=variant_color)


    return render(request, 'server/partials/product/update-product-details.html', {
        'product': product,
        'product_variant': product_variant,
        'images': images
    })

def update_quantity(request, product_variant_id, option, quantity):
    product_variant = ProductVariant.objects.get(id=product_variant_id)
    error = ''
    product = product_variant.product

    if option == 'increase':
        quantity += 1
    elif option == 'decrease':
        quantity -= 1

    if quantity > product_variant.stock:
        error = 'Out of Stock - Decrease Quantity'

    if quantity < 1:
        error = 'Quantity cannot be less than 1'

    

    total_price = product_variant.discount_price * quantity

    return render(request, 'server/partials/product/update-total-price.html', {
        'quantity': quantity,
        'total_price': total_price,
        'product_variant': product_variant,
        'product':product,
        'error': error
    })

def sort_reviews(request, product_id, sort_by):
    product = Product.objects.get(id=product_id)
    reviews = Review.objects.filter(product=product, is_active=True)


    if sort_by == 'most_recent':
        reviews = reviews.order_by('-created_at')
    elif sort_by == 'oldest':
        reviews = reviews.order_by('created_at')
    elif sort_by == 'most_popular':
        reviews = reviews.order_by('-rating')

    return render(request, 'server/components/product_page/reviews-list.html', {
        'reviews': reviews
    })

def submit_review(request, product_id):
    
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        rating = request.POST.get('rate')
        review = request.POST.get('review')
        title = request.POST.get('title')
        user = request.user


    review = Review.objects.create(
        user=user,
        product=product,
        title=title,
        review=review,
        rating=rating,
    )


    return redirect(request.META.get("HTTP_REFERER", "/")) 

# wishlist views

def wishlist_page(request):

    
    if not request.user.is_authenticated:
        return redirect("login")
    
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
    products_list = [item.product for item in wishlist_items]

    return render(request, 'server/wishlist.html', {'products': products_list})

def add_remove_wishlist_item(request, product_id):
    
    if not request.user.is_authenticated:
        response = HttpResponse()
        response["HX-Redirect"] = "/login/"  # Redirect to login if not authenticated
        return response
    
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    in_wishlist = True
    # if item is already in wishlist, remove it
    if not created:
        wishlist_item.delete()
        in_wishlist = False

    return render(request, 'server/partials/wishlist/wishlist-icon.html', {
        'in_wishlist': in_wishlist,
        'product':product
    })

def add_remove_wishlist_item_product_page(request, product_id):
    
    if not request.user.is_authenticated:
        response = HttpResponse()
        response["HX-Redirect"] = "/login/"  # Redirect to login if not authenticated
        return response

    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    in_wishlist = True
    # if item is already in wishlist, remove it
    if not created:
        wishlist_item.delete()
        in_wishlist = False

    return render(request, 'server/partials/product/wishlist-icon.html', {
        'in_wishlist': in_wishlist,
        'product':product
    })

def remove_item_from_wishlist(request, product_id):
    
    if not request.user.is_authenticated:
        response = HttpResponse()
        response["HX-Redirect"] = "/login/"  # Redirect to login if not authenticated
        return response
    
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, product=product)
    if wishlist_item:
        wishlist_item.delete()

    return render(request, 'server/partials/wishlist/wishlist-count.html')

# cart views

def remove_sidebar_cart_item(request, product_varaint_id):
    product_variant = ProductVariant.objects.filter(id=product_varaint_id).first()
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product_variant=product_variant)
    cart_item.delete()
    
    return render(request, 'server/partials/cart/update-sidebar-cart-sub-total.html')

def update_cart_count(request):
    if not request.user.is_authenticated:
        return 0
    
    cart, _  = Cart.objects.get_or_create(user=request.user)    
    cart_count =  cart.cart_items.count() if cart else 0
    return HttpResponse(str(cart_count))  # Return the cart count as a plain text response

def update_cart_sub_total(request):
    if not request.user.is_authenticated:
        return 0
    
    cart, _ = Cart.objects.get_or_create(user=request.user)

    sub_total = cart.total_price_pre_tax
    
    return HttpResponse(str(sub_total))  # Return the cart count as a plain text response


def add_cart_item(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    
    selected_size = request.GET.get('size')
    selected_color = request.GET.get('color')

    default_color = request.GET.get('selected_color')
    default_size = request.GET.get('selected_size')
    
    print(f"Quantity is {quantity}")
    
    variant_color = selected_color or default_color
    variant_size = selected_size or default_size
    product_variant = ProductVariant.objects.filter(product=product,color__iexact=variant_color, size__iexact=variant_size).first()
    
    if product_variant.stock < quantity:
        error = f"Out of Stock - Decrease Quantity"
        return render(request, 'server/partials/cart/error-message.html', {
            'error': error
        })

    cart, _ = Cart.objects.get_or_create(user=request.user)
    # creating cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=product_variant)
    
    if not created:
        cart_item.quantity += quantity  # Increase quantity if item already exists
        print(f"Cart Updated == {cart_item.quantity}")
    else:
        cart_item.quantity = quantity 
        print("Cart not udpated!")

    cart_item.save()
    # show go to cart and update the cart list
    varaint = {"details": product_variant, "quantity": quantity}
    time.sleep(1)
    return render(request, 'server/partials/shop/update-sidebar-cart.html', {
        'product': product,
        'varaint': varaint,
    })
    
    
def cart_page(request):
    # header tags
    men_tags =  Tag.objects.filter(category__name='Men', is_active=True)    
    women_tags =  Tag.objects.filter(category__name='Women', is_active=True)    
    kids_tags =  Tag.objects.filter(category__name='Kids', is_active=True)    
    header_products = Product.objects.filter(is_active=True, tags__name='Best Seller')[:2]
    current_tab = ''
    # context data
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all().order_by('-id')  
    reviews = Review.objects.filter(user=request.user)[:4]
    people_also_bought = Product.objects.filter(is_active=True, tags__name='Best Seller')[:5]
    print(reviews)
    return render(request, 'server/cart.html', 
    {
        'men_tags': men_tags,
        'women_tags': women_tags,
        'kids_tags': kids_tags,
        'header_products': header_products,
        'current_tab': current_tab,
        'cart_items': cart_items,
        'cart': cart,
        'reviews': reviews,
        'people_also_bought': people_also_bought
    })

def remove_cart_item(request, product_varaint_id):
    product_variant = ProductVariant.objects.filter(id=product_varaint_id).first()
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product_variant=product_variant)
    cart_item.delete()

    cart_item_length = CartItem.objects.filter(cart=cart).count()
    sub_total = cart.total_price_pre_tax
    free_shipping_remaining = cart.free_shipping_remaining
    
    return render(request, 'server/partials/cart/update-cart-sub-total.html',{
        'cart': cart,
        'cart_item_length': cart_item_length,
        'sub_total': sub_total,
        'free_shipping_remaining': free_shipping_remaining
    })

def cart_update_quantity(request, product_varaint_id, option):
    product_variant = ProductVariant.objects.filter(id=product_varaint_id).first()
    error = ''
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product_variant=product_variant).first()

    quantity = cart_item.quantity

    if option == 'increase':
        quantity += 1
    elif option == 'decrease':
        quantity -= 1

    if quantity > product_variant.stock:
        error = 'Out of Stock - Decrease Quantity'

    if quantity < 1:
        error = 'Quantity cannot be less than 1'

    if not error:
        cart_item.quantity = quantity
        cart_item.save()
    
    if error:
        print(f"Error is {error}")
        return render(request, 'server/partials/cart/error-message.html', {
            'error': error
        })

    print(f"Cart Updated == {cart_item.quantity}")
    return render(request, 'server/partials/cart/update-cart-item-quantity.html', {
        'item': cart_item,
        'cart': cart,
    })

def checkout_page(request):

    user = request.user

    if not user.is_authenticated:
        return redirect("login")
    
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect("cart")

    need_gift_wrap = request.GET.get("gift_wrap", "0") == "1"
    order_note = request.GET.get("note", "").strip()

    cart_total = float(cart.cart_total) + (99.00 if need_gift_wrap else 0)

    cart_total = f"{math.ceil(cart_total):.2f}"

    user_addresses = UserAddress.objects.filter(user=user)
    
    return render(request, 'server/checkout.html',{
        'cart_items': cart_items,
        'cart': cart,
        'need_gift_wrap': need_gift_wrap,
        'order_note': order_note,
        'cart_total': cart_total,
        'user_addresses': user_addresses
    })

def add_address(request):
    print('working')
    user = request.user
    name = request.GET.get('name')
    street_address = request.GET.get('street_address')
    city = request.GET.get('city')
    state = request.GET.get('state')
    postal_code = request.GET.get('postal_code')
    country = request.GET.get('country')
    mobile_number = request.GET.get('mobile_number')
    address_nickname = request.GET.get('address_nickname')
    email = request.GET.get('email')
    
    address = UserAddress.objects.create(
        user=user,
        name=name,
        street_address=street_address,
        city=city,
        state=state,
        postal_code=postal_code,
        country=country,
        mobile_number=mobile_number,
        address_nickname=address_nickname,
        email=email
    )
    return render(request, 'server/partials/checkout/user-address.html', {
        'address': address
    })


def apply_coupon_code(request, gift_wrap):
    user = request.user
    coupon_code = request.GET.get('coupon_code')
    print(coupon_code)
    gift_wrap = bool(gift_wrap)
    print(gift_wrap)
    coupon = Coupon.objects.filter(coupon_code=coupon_code).first()

    if not coupon or coupon.is_active == False:
        error = f"Coupon code is not valid"
        return render(request, 'server/partials/cart/error-message.html', {
            'error': error
        })

    cart = Cart.objects.get(user=user)
    sub_total = cart.total_price_pre_tax

    if sub_total < coupon.min_order_amount:
        error = f"Minimum order value should be {coupon.min_order_amount}"
        return render(request, 'server/partials/cart/error-message.html', {
            'error': error
        })
    

    flat_discount = coupon.discount_amount
    discount_percent = coupon.discount_percentage

    if flat_discount:
        sub_total, tax, final_total = calculate_cart_total(cart, flat_discount).values()
        if gift_wrap:
            final_total = final_total + Decimal("99.00")
        print(sub_total, tax, final_total)

        return render(request, 'server/partials/checkout/update-checkout-prices.html',{
        'sub_total': sub_total,
        'tax':tax,
        'final_total': final_total,
        'gift_wrap': gift_wrap,
        'discount': discount_amount
        })

    if discount_percent:
        discount_amount = f"{math.ceil((discount_percent / 100) * sub_total):.2f}"

        if Decimal(discount_amount) > coupon.max_discount_amount:
            discount_amount = f"{coupon.max_discount_amount:.2f}"


        sub_total, tax, final_total = calculate_cart_total(cart, discount_amount).values()
        if gift_wrap:
            final_total = final_total + Decimal("99.00")
        print(sub_total, tax, final_total)

        return render(request, 'server/partials/checkout/update-checkout-prices.html',{
        'sub_total': sub_total,
        'tax':tax,
        'final_total': final_total,
        'gift_wrap': gift_wrap,
        'discount': discount_amount
        })


# order views
# TODO: add need_gift_wrap amount (99) to final total and order note
def create_order(request, need_gift_wrap, order_note):
    user = request.user

    if not user.is_authenticated:
        return redirect("login")

    cart, _ = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect("cart")

    
    shipping_address_id = request.POST.get('selected_address')
    shipping_address = UserAddress.objects.filter(id=shipping_address_id).first()
    billing_address_id = request.POST.get('billing_address') or shipping_address.id
    billing_address = UserAddress.objects.filter(id=billing_address_id).first()
    
    shipping_cost = request.POST.get('shipping_cost') or 0
    coupon_code = request.POST.get('coupon_code') or ''
    discount_amount = 0

    if coupon_code != '':
        coupon = Coupon.objects.filter(coupon_code=coupon_code).first()
        if coupon:
            discount_amount = calculate_discount(coupon, cart)
        

    sub_total, tax, final_total = calculate_cart_total(cart, discount_amount).values()

    # use transactions for atomicity
    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            order_date=timezone.now(),
            shipping_cost=shipping_cost,
            order_status='ordered',
            shipping_address=shipping_address,
            billing_address=billing_address,
            total_price_pre_tax=sub_total,
            total_tax=tax,
            order_total=final_total,
            discount=discount_amount,
            coupon_code=coupon_code,
        )

        for item in cart_items:
            product_variant = ProductVariant.objects.filter(id=item.product_variant.id).first()
            product_variant.stock -= item.quantity
            product_variant.save()
            OrderItem.create_order_item(order, item.product_variant, item.quantity)

        cart.delete()

        return redirect("order-success")
    
    return redirect("order-failure")

def order_success(request):
    return render(request, 'server/components/checkout/order-success.html')

def order_failure(request):
        return render(request, 'server/components/checkout/order-failure.html')