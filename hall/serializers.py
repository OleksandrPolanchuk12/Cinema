from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework import serializers
from .models import Hall

class HallSerializer(ModelSerializer):
    class Meta:
        model = Hall
        fields = ['name', 'capacity', 'row', 'seat', 'cinema']

class SeatReservationSerializer(Serializer):
    row = serializers.CharField(max_length=20)
    seat = serializers.IntegerField()

    def validate(self, data):
        row = data.get('row')
        seat_number = data.get('seat')
        hall = self.context.get('hall')

        if not hall:
            raise serializers.ValidationError('Hall is required fro validation')

        rows = hall.row.get('rows', [])
        if row not in rows:
            raise serializers.ValidationError(f'Row {row} not found in hall')

        seats = hall.seat.get(row)
        for seat in seats:
            if seat['number'] == seat_number:
                if seat.get('reserved'):
                    raise serializers.ValidationError(f'Seat {seat_number} is already reserved')
                return data
        raise serializers.ValidationError(f'Seat {seat_number} not found in row {row}')
