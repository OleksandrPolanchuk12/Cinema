from django.db import models
from cinema.models import Cinema

class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    row = models.JSONField()
    seat = models.JSONField()
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        total = 0
        for i in self.seat.values:
            total += len(i)
        self.capacity = total
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name