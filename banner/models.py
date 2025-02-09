from django.db import models
from product.models import Tag, ProductVariant
from django.utils import timezone
from product.models import SubCategory


# Women Banner Tables
class WomenBanner(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='women-banners/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='women_banners', null=True, blank=True, limit_choices_to={'category__name': 'Women'})
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class WomenCollection(models.Model):
    title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='collections/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='women_collections', null=True, blank=True, limit_choices_to={'category__name': 'Women'})
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class WomenFeaturedProduct(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    quote_text = models.CharField(max_length=512)
    image = models.ImageField(upload_to='featured_products/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='women_featured_products', null=True, blank=True, limit_choices_to={'category__name': 'Women'})
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title 

class WomenMidBanner(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='mid_banners/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='women_mid_banners', null=True, blank=True, limit_choices_to={'category__name': 'Women'})
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

# Man Banner tables
class MenBanner(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='men_banners', null=True, blank=True, limit_choices_to={'product__category__name': 'Men'})
    image = models.ImageField(upload_to='men-banners/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_variant.product.name

class MenCollection(models.Model):
    title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='collections/')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='men_collections', null=True, blank=True, limit_choices_to={'category__name': 'Men'})
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class MenFeaturedProduct(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    quote_text = models.CharField(max_length=512)
    image = models.ImageField(upload_to='featured_products/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='men_featured_products', null=True, blank=True, limit_choices_to={'category__name': 'Men'})
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title   

class MenMidBanner(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='mid_banners/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='men_mid_banners', null=True, blank=True, limit_choices_to={'category__name': 'Men'})
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class MenCountdown(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    button_text = models.CharField(max_length=512)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='countdown/',default='countdown/default.jpg')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='men_countdown', null=True, blank=True, limit_choices_to={'category__name': 'Men'})

    @property
    def time_left(self):
        """Calculate and return the time remaining until end_date in seconds"""
        now = timezone.now()
        if now > self.end_date:
            return 0
        time_diff = self.end_date - now
        return int(time_diff.total_seconds())

    def __str__(self):
        return self.title

class MenBarText(models.Model):
    text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text
    
# Kids Banner tables
class KidsBanner(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='kids-banners/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='kids_banners', null=True, blank=True, limit_choices_to={'category__name': 'Kids'})
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title 

class KidsCollection(models.Model):
    title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='collections/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='kids_collections', null=True, blank=True, limit_choices_to={'category__name': 'Kids'})
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class KidsFeaturedProduct(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    quote_text = models.CharField(max_length=512)
    image = models.ImageField(upload_to='featured_products/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='kids_featured_products', null=True, blank=True, limit_choices_to={'category__name': 'Kids'})
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title  
    
class KidsMidBanner(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='mid_banners/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='kids_mid_banners', null=True, blank=True, limit_choices_to={'category__name': 'Kids'})
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title