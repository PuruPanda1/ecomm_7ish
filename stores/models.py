from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=512)
    store_address = models.CharField(max_length=512)
    store_city = models.CharField(max_length=512)
    store_state = models.CharField(max_length=512)
    store_country = models.CharField(max_length=512)
    store_zip_code = models.CharField(max_length=512)
    store_email = models.EmailField()
    store_phone = models.CharField(max_length=512)
    store_timings = models.CharField(max_length=512) # Example Mon - Fri: 9:00 - 18:00
    store_image = models.ImageField(upload_to='stores/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name