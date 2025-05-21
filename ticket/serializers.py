from rest_framework import serializers
from rest_framework.serializers import Serializer
from .models import Ticket


class SeatReservationSerializer(Serializer):
    row = serializers.CharField(max_length=20)
    seat = serializers.IntegerField()

    def validate(self, data):
        row = data.get('row')
        seat_number = data.get('seat')
        show_unit = self.context.get('show_unit')

        if not show_unit:
            raise serializers.ValidationError('ShowUnit is required for validation')

        if Ticket.objects.filter(row=row, seat_number=seat_number, show_unit=show_unit).exists():
            raise serializers.ValidationError('This seat is already taken')

        return  data

