from rest_framework import serializers
from rest_framework.serializers import Serializer
from .models import Ticket
from cinema.models import Cinema
from django.shortcuts import get_object_or_404


class SeatReservationSerializer(Serializer):
    row = serializers.CharField(max_length=20)
    seat = serializers.IntegerField()

    def validate(self, data):
        row = data.get('row')
        seat_number = data.get('seat')
        show_unit = self.context.get('show_unit')
        cinema =  get_object_or_404(Cinema, id=self.context.get('cinema_id'))

        if not cinema:
            raise serializers.ValidationError('Cinema is required for validation')

        if not show_unit:
            raise serializers.ValidationError('ShowUnit is required for validation')

        show_cinema = show_unit.show.hall.cinema
        if cinema != show_cinema:
            raise serializers.ValidationError(f'ShowUnit {show_unit} does not exists into cinema {cinema}')

        if Ticket.objects.filter(row=row, seat_number=seat_number, show_unit=show_unit).exists():
            raise serializers.ValidationError('This seat is already taken')

        return  data


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['show_unit', 'row', 'seat_number']