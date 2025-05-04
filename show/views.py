from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ShowSerializer
from django.utils import timezone
from hall.models import Hall
from cinema.models import Cinema
from .models import Show

class CurrentDayShowAPIView(APIView):
    def get(self, request, cinema_id):
        now = timezone.now()
        cinema = get_object_or_404(Cinema, id=cinema_id)
        halls = get_list_or_404(Hall, cinema=cinema)
        shows = []

        for hall in halls:
            showtimes = get_list_or_404(Show, hall=hall, showtime__date=now.date(), showtime__time__gt=now.time()) 
            shows.append(ShowSerializer(showtimes, many=True).data)
        return Response({'shows': shows})
