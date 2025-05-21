from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from show.models import ShowUnit


class Ticket(models.Model):
    show_unit = models.ForeignKey(ShowUnit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    row = models.CharField(max_length=20)
    seat_number = models.IntegerField()

    class Meta:
        unique_together = ('show_unit', 'row', 'seat_number')

    def save(self, *args, **kwargs):
        hall = self.show_unit.show.hall
        seats_hall = hall.seat

        if self.row not in seats_hall:
            raise ValidationError(f"Row {self.row} does not exists")

        seats = any(seat['number'] == self.seat_number for seat in seats_hall[self.row])
        if not seats:
            raise ValidationError(f'Seat {self.seat_number} does not exists')
        super().save(*args, **kwargs)
