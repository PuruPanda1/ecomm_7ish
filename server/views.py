from django.shortcuts import render
from banner.models import Banner, Collection, FeaturedProduct, MidBanner
from product.models import Product

def home(request):
    banners = Banner.objects.filter(is_active=True)
    first, second, third, fourth = Collection.objects.filter(is_active=True)[:4]
    featured_product = FeaturedProduct.objects.filter(is_active=True).first()
    best_sellers = Product.objects.filter(tags__name='Best Seller' , is_active=True)
    mid_banner = MidBanner.objects.filter(is_active=True)[:2]
    return render(request, 'server/home.html', {'banners': banners, 'first': first, 'second': second, 'third': third, 'fourth': fourth, 'featured_product': featured_product, 'best_sellers': best_sellers, 'mid_banner': mid_banner})

# using tag to show the banner of the shops page and sub_title to show the sub_title of the shops page
def shop(request, tag, sub_title):
    if tag is None:
        tag = 'New Arrival'
    if sub_title is None:
        sub_title = 'Shop through our latest selection of Fashion'


    products = Product.objects.filter(tags__name=tag)
    return render(request, 'server/shop.html', {
        'title': tag,
        'sub_title': sub_title,
        'products': products
    })