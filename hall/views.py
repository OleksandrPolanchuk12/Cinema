from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListAPIView

from cinema.models import Cinema
from .models import Hall
from .serializers import HallSerializer


class HallCinemaListAPIView(ListAPIView):
    serializer_class = HallSerializer

    def get_queryset(self):
        cinema = get_object_or_404(Cinema, id=self.kwargs['cinema_id'])
        return Hall.objects.filter(cinema=cinema)


class SingleHallAPIView(RetrieveAPIView):
    serializer_class = HallSerializer

    def get_object(self):
        return get_object_or_404(Hall, id=self.kwargs['hall_id'], cinema=self.kwargs['cinema_id'])
