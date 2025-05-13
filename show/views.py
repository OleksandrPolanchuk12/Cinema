from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ShowSerializer
from django.utils import timezone
from hall.models import Hall
from cinema.models import Cinema
from .models import Show
from rest_framework import  status
from datetime import datetime

class CurrentDayShowAPIView(APIView):
    def post(self, request, cinema_id):
        show_start_data = request.data.get('show_start', "")
        show_end_data = request.data.get('show_end', "")
        try:
            if show_start_data:
                show_start = datetime.fromisoformat(show_start_data)
            else:
                return Response({'message':'Missing show_start parameter'}, status=status.HTTP_400_BAD_REQUEST)
            if show_end_data:
                show_end = datetime.fromisoformat(show_end_data)
            else:
                show_end = None
        except ValueError:
            return Response({'message':'Invalid datetime format'}, status=status.HTTP_400_BAD_REQUEST)

        cinema = get_object_or_404(Cinema, id=cinema_id)
        halls = get_list_or_404(Hall, cinema=cinema)
        shows = []
        now = timezone.now()

        for hall in halls:
            if show_end:
                showtimes = get_list_or_404(Show, hall=hall, showtime__range=(show_start,show_end))
            else:
                if show_start.date() == now.date():
                    showtimes = get_list_or_404(Show,hall=hall, showtime__date=show_start.date(),
                                                showtime__time__gt=now.time())
                else:
                    showtimes = get_list_or_404(Show,hall=hall, showtime__date=show_start.date())
            shows.append(ShowSerializer(showtimes, many=True).data)
        if not shows:
            return Response({'message':'Shows is ended'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'shows': shows}, status=status.HTTP_200_OK)
