from .serializers import CinemaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cinema

class CinemaListView(APIView):
    def get(self, request, *args, **kwargs):
        cinema = Cinema.objects.all()
        return Response({
            'cinemas': CinemaSerializer(cinema, many=True).data
        })
        