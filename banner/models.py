from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='banners/')
    tag = models.CharField(max_length=512, default='Trending')
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Collection(models.Model):
    title = models.CharField(max_length=512)
    image = models.ImageField(upload_to='collections/')
    tag = models.CharField(max_length=512, default='Trending')
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class FeaturedProduct(models.Model):
    title = models.CharField(max_length=512)
    sub_title = models.CharField(max_length=512)
    quote_text = models.CharField(max_length=512)
    image = models.ImageField(upload_to='featured_products/')
    tag = models.CharField(max_length=512, default='Trending')
    button_text = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title   

