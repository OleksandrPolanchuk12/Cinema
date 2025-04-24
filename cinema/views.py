from .serializers import CinemaSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Cinema

class CinemaListAPIView(ListAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer