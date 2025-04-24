from django.db import models

class Cinema(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name