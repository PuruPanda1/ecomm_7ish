from django.db import models
from product.models import Tag
class WomenBanner(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='women-banners/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='women_banners', null=True, blank=True, limit_choices_to={'category__name': 'Women'})
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class MenBanner(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='men-banners/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='men_banners', null=True, blank=True, limit_choices_to={'category__name': 'Men'})
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
    
class MenCollection(models.Model):
    title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='collections/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='men_collections', null=True, blank=True, limit_choices_to={'category__name': 'Men'})
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

class WomenMidBanner(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='mid_banners/')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='women_mid_banners', null=True, blank=True, limit_choices_to={'category__name': 'Women'})
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