from django.db import models
from movie.models import Movie
from hall.models import Hall
from django.utils import timezone

class Show(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE) 
    showtime = models.DateTimeField(default=None)
    start_show = models.DateField(null=True,blank=True)
    end_show = models.DateField(null=True,blank=True)
    prices= models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.movie.title} - {self.hall.name}"
    