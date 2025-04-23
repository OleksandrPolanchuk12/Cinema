from django.db import models
from hall.models import Hall

class Cinema(models.Model):
    name = models.CharField(max_leghth=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name