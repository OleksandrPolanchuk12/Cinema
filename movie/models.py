from django.db import models
from hall.models import Hall

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.DurationField()
    poster = models.ImageField(upload_to='media/posters/')

    def __str__(self):
        return self.title