from datetime import datetime

from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models import Cinema
from hall.models import Hall
from .models import Show, ShowUnit
from .serializers import ShowUnitSerializer, ShowSerializer, CurrentShowDaySerializer


class CurrentDayShowAPIView(APIView):
    @swagger_auto_schema(request_body=CurrentShowDaySerializer)
    def post(self, request, cinema_id):
        serializer = CurrentShowDaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        show_end = serializer.validated_data['show_end_data']
        show_start = serializer.validated_data['show_start_data']

        cinema = get_object_or_404(Cinema, id=cinema_id)
        halls = get_list_or_404(Hall, cinema=cinema)

        now = timezone.localtime()
        shows = []

        for hall in halls:
            show = Show.objects.filter(hall=hall)
            for show_obj in show:
                show_unit = ShowUnit.objects.filter(show=show_obj, showtime__gte=show_obj.start_show,
                                                    showtime__lte=show_obj.end_show)
                if show_end:
                    showtimes = show_unit.filter(showtime__range=(show_start, show_end), showtime__gt=now)
                if not show_end and show_start.date() == now.date():
                    showtimes = show_unit.filter(showtime__date=show_start.date(), showtime__gt=now)
                if not show_end and show_start.date() != now.date():
                    showtimes = show_unit.filter(showtime__date=show_start.date())

                if showtimes:
                    shows.extend(ShowUnitSerializer(showtimes, many=True).data)

        if not shows:
            return Response({'message': 'Shows is ended'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'shows': shows}, status=status.HTTP_200_OK)


class ShowDetailAPIView(RetrieveAPIView):
    serializer_class = ShowSerializer
    queryset = Show.objects.all()
