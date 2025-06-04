from django.shortcuts import get_object_or_404, get_list_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models import Cinema
from hall.models import Hall
from show.models import ShowUnit
from user.models import User
from .models import Ticket
from .serializers import SeatReservationSerializer, TicketSerializer, FreeSeatsSerializer


class SeatReservationAPIView(APIView):
    @swagger_auto_schema(request_body=SeatReservationSerializer)
    def post(self, request, *args, **kwargs):
        show_id = kwargs['show_id']
        show_unit = get_object_or_404(ShowUnit, id=show_id)
        serializer_data = SeatReservationSerializer(data=request.data, context={'show_unit': show_unit,
                                                                                'cinema_id': kwargs['cinema_id']})
        if not serializer_data.is_valid():
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        row = serializer_data.validated_data['row']
        seat_number = serializer_data.validated_data['seat']

        ticket = Ticket.objects.create(row=row, seat_number=seat_number, show_unit=show_unit, user=request.user)
        return Response({
            'message': f'Seat {seat_number} in row {row} successfully reserved'},
            status=status.HTTP_201_CREATED
        )


class FreeSeatsAPIView(APIView):
    def get(self, request, **kwargs):
        cinema = get_object_or_404(Cinema, id=kwargs['cinema_id'])
        hall = get_object_or_404(Hall, id=kwargs['hall_id'])
        show_unit = get_object_or_404(ShowUnit, id=kwargs['show_unit_id'])
        tickets = get_list_or_404(Ticket, show_unit=show_unit)
        context = {
            'cinema': cinema,
            'hall': hall,
            'show_unit': show_unit
        }
        serializer = FreeSeatsSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        seats = hall.seat

        for ticket in tickets:
            row_name = ticket.row
            seat_number = ticket.seat_number

            row = seats.get(row_name)
            for seat in row:
                if seat["number"] == str(seat_number):
                    seat["reserved"] = True
                    break
        return Response({'free_seats': seats}, status=status.HTTP_200_OK)


class TicketListAPIView(ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        return Ticket.objects.filter(user=user)
