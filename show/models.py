from django.db import models
from movie.models import Movie
from hall.models import Hall

class Show(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE) 
    showtimes = models.JSONField(default={"0000-00-00": []})
    prices= models.JSONField(default={"standard": 150,"vip": 250})
    
    def __str__(self):
        return f"{self.movie.title} - {self.hall.name}"
    
