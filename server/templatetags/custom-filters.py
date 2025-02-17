from django import template
from reviews.models import Review
from wishlist.models import WishlistItem, Wishlist
from cart.models import Cart, CartItem
from django.db.models import Avg
from collections import Counter
from product.models import Product

register = template.Library()

@register.filter
def unique_colors(images):
    seen_colors = set()
    unique_images = []
    
    for image in images:
        if image.color and image.color.lower() not in seen_colors:
            seen_colors.add(image.color.lower())
            unique_images.append(image)
    
    return unique_images


class ProductVariantData:
    """Custom class to store product variant details."""
    def __init__(self, color, image):
        self.color = color
        self.image = image
        self.sizes = []
        self.prices = {}

    def add_variant(self, size, price):
        """Add size and price to the variant."""
        if size not in self.sizes:
            self.sizes.append(size)
        self.prices[size] = price

@register.filter
def get_product_variants(product):
    """Custom filter to fetch variants for a given product."""
    color_variants = {}

    # Get all product variants related to the given product
    product_variants = product.variants.filter(product=product)  # Assuming `variants` is a related name in the model
    product_images = product.images.all()


    for variant in product_variants:
        color = variant.color
        if color not in color_variants:
            color_variants[color] = ProductVariantData(color, product_images.filter(color__iexact=color).first().image.url)

        color_variants[color].add_variant(variant.size, variant.discount_price)


    return list(color_variants.values())  # Convert dict to list for template use


@register.filter
def get_average_rating(reviews):
    if reviews.count() > 0:
        return reviews.aggregate(Avg('rating'))['rating__avg']
    return 0


@register.filter
def get_reviews_count(reviews):
    return reviews.count()



@register.filter
def rating_distribution(reviews):
    if not reviews:
        return {}

    # Count occurrences of each rating
    ratings_count = Counter([review.rating for review in reviews])

    # Total number of reviews
    total_reviews = sum(ratings_count.values())

    # Ensure total_reviews is not zero before division
    if total_reviews == 0:
        return {}

    # Prepare the dictionary with rating and percentage
    distribution = {
        i: {
            'count': ratings_count.get(i, 0),
            'percentage': round((ratings_count.get(i, 0) / total_reviews) * 100, 2)
        }
        for i in range(5, 0, -1)  # Iterate from 5-star to 1-star
    }

    return distribution 


@register.filter
def in_wishlist(product, user):
    if not user.is_authenticated:
        return False
    return WishlistItem.objects.filter(wishlist__user=user, product=product).exists()

@register.filter
def get_wishlist_count(user):
    if not user.is_authenticated:
        return 0
    wishlist, created  = Wishlist.objects.get_or_create(user=user)
    return wishlist.wishlist_items.count() if wishlist else 0

# cart filters

@register.filter
def get_cart_count(user):
    if not user.is_authenticated:
        return 0
    cart, created  = Cart.objects.get_or_create(user=user)
    return cart.cart_items.count() if cart else 0

@register.filter
def get_cart_items(user):
    if not user.is_authenticated:
        return ''
   
    cart, _ = Cart.objects.get_or_create(user=user)

    cart_items = CartItem.objects.filter(cart=cart)
    product_variant_list = [
        {"details": item.product_variant, "quantity": item.quantity} 
        for item in cart_items
    ]
    
    return product_variant_list

@register.filter
def get_cart_sub_total(user):
    if not user.is_authenticated:
        return ''
   
    cart, created = Cart.objects.get_or_create(user=user)

    sub_total = cart.total_price_pre_tax
    
    return sub_total

@register.filter
def get_suggestion(user):
    products_list = Product.objects.filter(tags__name__iexact ='Best Seller')
    return products_list

@register.filter
def product_price(discount_price, quantity):
    return (discount_price * quantity)