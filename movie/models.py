from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models
import os
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    age_restrictions = models.CharField(max_length=10)
    director = models.CharField(max_length=100)
    genres = models.CharField(max_length=255)
    release_date = models.DateField()
    duration = models.DurationField()
    poster = models.ImageField(upload_to=f'media/posters/')

    def save(self, *args, **kwargs):
        if self.poster:
            self.poster.name = f'{self.title}_{self.release_date}.jpg'
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
@receiver(post_delete, sender=Movie)
def delete_poster(sender, instance, **kwargs):
    if instance.poster:
        if os.path.isfile(instance.poster.path):
            os.remove(instance.poster.path)