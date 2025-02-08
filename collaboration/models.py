from django.db import models

class Collaboration(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='collaboration/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
