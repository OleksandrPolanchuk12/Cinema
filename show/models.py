from django.db import models

from hall.models import Hall
from movie.models import Movie


class Show(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_show = models.DateTimeField()
    end_show = models.DateTimeField()
    prices = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.movie.title} - {self.hall.name}"


class ShowUnit(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    showtime = models.DateTimeField()

    def __str__(self):
        return f"{self.show.movie.title} - {self.showtime} - {self.show.hall.name}"
