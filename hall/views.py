from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models import Cinema
from .models import Hall
from .serializers import HallSerializer, SeatReservationSerializer


class SeatReservationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        hall_id = kwargs['hall_id']
        hall = get_object_or_404(Hall, id=hall_id)
        serializer_data = SeatReservationSerializer(data=request.data, context={'hall': hall})
        if not serializer_data.is_valid():
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        row = serializer_data.validated_data['row']
        seat_number = serializer_data.validated_data['seat']
        seats = hall.seat.get(row)

        for seat in seats:
            if seat['number'] == seat_number:
                seat['reserved'] = True
                hall.save()
                return Response({
                    'message': f'Seat {seat_number} in row {row} successfully reserved'},
                    status=status.HTTP_201_CREATED
                )

        return Response({})


class HallCinemaListAPIView(ListAPIView):
    serializer_class = HallSerializer

    def get_queryset(self):
        cinema = get_object_or_404(Cinema, id=self.kwargs['cinema_id'])
        return Hall.objects.filter(cinema=cinema)


class SingleHallAPIView(RetrieveAPIView):
    serializer_class = HallSerializer

    def get_object(self):
        return get_object_or_404(Hall, id=self.kwargs['hall_id'], cinema=self.kwargs['cinema_id'])
