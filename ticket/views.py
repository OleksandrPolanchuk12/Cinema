from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from show.models import ShowUnit
from .models import Ticket
from .serializers import SeatReservationSerializer


class SeatReservationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        show_id = kwargs['show_id']
        show_unit = get_object_or_404(ShowUnit, id=show_id)
        serializer_data = SeatReservationSerializer(data=request.data, context={'show_unit': show_unit})

        if not serializer_data.is_valid():
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        row = serializer_data.validated_data['row']
        seat_number = serializer_data.validated_data['seat']

        ticket = Ticket.objects.create(row=row, seat_number=seat_number, show_unit=show_unit, user=request.user)
        return Response({
            'message': f'Seat {seat_number} in row {row} successfully reserved'},
            status=status.HTTP_201_CREATED
        )
