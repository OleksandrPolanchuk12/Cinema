from django.db import models

class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    row = models.JSONField()
    seat = models.JSONField()

    def __str__(self):
        return self.name