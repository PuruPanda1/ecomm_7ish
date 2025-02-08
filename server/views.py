from django.shortcuts import render
from product.models import Product



def home(request):
    return render(request, 'server/home.html')

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