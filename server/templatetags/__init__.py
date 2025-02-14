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
