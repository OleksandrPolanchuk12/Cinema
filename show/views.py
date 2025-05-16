from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .serializers import ShowSerializer
from django.utils import timezone
from hall.models import Hall
from cinema.models import Cinema
from .models import Show
from rest_framework import  status
from datetime import datetime
from django.db.models import F

class CurrentDayShowAPIView(APIView):
    def post(self, request, cinema_id):
        show_start_data = request.data.get('show_start', "")
        show_end_data = request.data.get('show_end', "")
        try:
            show_end = None
            if not show_start_data:
                return Response({'message': 'Missing show_start parameter'}, status=status.HTTP_400_BAD_REQUEST)
            show_start = datetime.fromisoformat(show_start_data)
            if show_end_data:
                show_end = datetime.fromisoformat(show_end_data)
        except ValueError:
            return Response({'message':'Invalid datetime format'}, status=status.HTTP_400_BAD_REQUEST)

        cinema = get_object_or_404(Cinema, id=cinema_id)
        halls = get_list_or_404(Hall, cinema=cinema)
        shows = []
        now = timezone.localtime()

        for hall in halls:
            showtimes = None
            if show_end:
                showtimes = Show.objects.filter( hall=hall, showtime__range=(show_start,show_end),
                                                showtime__date__gte=F('start_show'), showtime__date__lte=F('end_show'))
            if show_start.date() == now.date() and show_end is None:
                showtimes = Show.objects.filter(hall=hall, showtime__date=show_start.date(),showtime__gt=now,
                                                showtime__date__gte=F('start_show'),showtime__date__lte=F('end_show'))
            if show_start.date() != now.date and show_end is None:
                showtimes = Show.objects.filter(hall=hall, showtime__date=show_start.date(),
                                                showtime__date__gte=F('start_show'), showtime__date__lte=F('end_show'))
            if showtimes:
                shows.extend(ShowSerializer(showtimes, many=True).data)
        if not shows:
            return Response({'message':'Shows is ended'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'shows': shows}, status=status.HTTP_200_OK)

class ShowDetailAPIView(RetrieveAPIView):
    serializer_class = ShowSerializer
    queryset = Show.objects.all()