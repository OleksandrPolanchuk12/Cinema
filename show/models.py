from django.db import models
from movie.models import Movie
from hall.models import Hall

class Show(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE) 
    showtime = models.DateTimeField(default=None)
    prices= models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.movie.title} - {self.hall.name}"
    