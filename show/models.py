from django.db import models

from hall.models import Hall
from movie.models import Movie
from django.core.exceptions import ValidationError
from datetime import timedelta


class Show(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_show = models.DateTimeField()
    end_show = models.DateTimeField()
    prices = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.movie.title} - {self.hall.name}"

    def clean(self):
        shows = Show.objects.filter(movie=self.movie, start_show__lt=self.end_show, end_show__gt=self.start_show)

        if self.pk:
            shows = shows.exclude(pk=self.pk)

        if shows:
            raise ValidationError('This show overlaps with another show in the sane hall')


class ShowUnit(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    showtime = models.DateTimeField()

    def __str__(self):
        return f"{self.show.movie.title} - {self.showtime} - {self.show.hall.name}"

    def clean(self):
        show_units = ShowUnit.objects.filter(show=self.show, show__hall=self.show.hall)
        showtime = self.showtime
        duration = self.show.movie.duration + timedelta(minutes=15)
        showtime_start = showtime - duration
        showtime_end = showtime + duration

        if self.pk:
            show_units = show_units.exclude(pk=self.pk)

        if ShowUnit.objects.filter(showtime__range=(showtime_start, showtime_end)):
            raise ValidationError(f'ShowUnit at overlaps with the previous one')



