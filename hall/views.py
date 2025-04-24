from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Hall
from cinema.models import Cinema
from .serializers import HallSerializer

class SeatReservationView(APIView):
    def get(self, request, *args, **kwargs):
        hall_id = kwargs['hall_id']
        hall = get_object_or_404(Hall, id=hall_id)
        return Response({
            'row': hall.row, 'seats': hall.seat
        })
    
    def post(self, request, *args, **kwargs):
        hall_id = kwargs['hall_id']
        row = request.data.get('row')
        seat_number = request.data.get('seat')
        hall = get_object_or_404(Hall, id=hall_id)
        message = ''

        seats = hall.seat.get(row)
        if seats:
            for seat in seats:
                if seat['number'] == int(seat_number):
                    if seat.get('reserved')==False:
                        seat['reserved'] = True
                        message = 'Seat reservation updated successfully.'
                    else:
                        message = f"Seat number {seat_number} is already reserved."
                    break
            else:
                message = f"Seat number {seat_number} not found."

            hall.save()
        else:
            message = f"Row {row} not found."


        return Response({
            'message': message
        })
    
class HallCinemaView(APIView):
    def get(self, request, *args, **kwargs):
        cinema = get_object_or_404(Cinema, id=kwargs['cinema_id'])
        halls = Hall.objects.filter(cinema = cinema)
        return Response({
            'halls': HallSerializer(halls, many=True).data
        })


