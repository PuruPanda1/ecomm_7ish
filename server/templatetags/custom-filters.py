from django import template

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

    print(list(color_variants.values()))

    return list(color_variants.values())  # Convert dict to list for template use
