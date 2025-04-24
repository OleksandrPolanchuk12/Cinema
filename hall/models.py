from django.db import models
from cinema.models import Cinema

class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(null=True, blank=True)
    row = models.JSONField()
    seat = models.JSONField()
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        total = 0
        for row, seat in self.seat.items():
            total += len(seat)
        self.capacity = total
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    # def reserved_seat(self, seat_number, row):
    #     seats = self.row.get(row, [])
    #     for seat in seats:
    #         if seat["number"] == seat_number:
    #             return "Reserved" if seat.get("reserved", False) else "No reserved"
    #     return "Місце не знайдено"