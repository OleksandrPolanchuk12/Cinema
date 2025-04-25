from django.db import models
from movie.models import Movie
from hall.models import Hall

class Show(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE) 
    start_data = models.DateTimeField()
    end_data = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} - {self.hall.name} - {self.start_data.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        self.end_data = self.start_data + self.movie.duration   
        super().save(*args, **kwargs)
