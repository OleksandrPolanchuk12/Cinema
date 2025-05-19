from datetime import datetime

from django.db.models import F
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models import Cinema
from hall.models import Hall
from .models import Show
from .serializers import ShowSerializer


class CurrentDayShowAPIView(APIView):
    def post(self, request, cinema_id):
        show_start_data = request.data.get('show_start', "")

        if not show_start_data:
            return Response({'message': 'Missing show_start parameter'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            show_start = datetime.fromisoformat(show_start_data)
        except ValueError:
            return Response({'message': 'Invalid datetime format'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            show_end = datetime.fromisoformat(request.data.get('show_end', "") or None)
        except ValueError:
            return Response({'message': 'Invalid datetime format'}, status=status.HTTP_400_BAD_REQUEST)

        cinema = get_object_or_404(Cinema, id=cinema_id)
        halls = get_list_or_404(Hall, cinema=cinema)

        now = timezone.localtime()
        shows = []

        for hall in halls:
            showtimes = Show.objects.filter(hall=hall, showtime__date__gte=F('start_show'),
                                            showtime__date__lte=F('end_show'))
            if show_end:
                showtimes = showtimes.filter(showtime__range=(show_start, show_end), showtime__gt=now)
            if not show_end and show_start.date() == now.date():
                showtimes = showtimes.filter(showtime__date=show_start.date(), showtime__gt=now)
            if not show_end and show_start.date() != now.date():
                showtimes = showtimes.filter(showtime__date=show_start.date())

            if showtimes:
                shows.extend(ShowSerializer(showtimes, many=True).data)

        if not shows:
            return Response({'message': 'Shows is ended'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'shows': shows}, status=status.HTTP_200_OK)


class ShowDetailAPIView(RetrieveAPIView):
    serializer_class = ShowSerializer
    queryset = Show.objects.all()
