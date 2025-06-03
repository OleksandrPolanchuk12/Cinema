from rest_framework.generics import RetrieveAPIView
from .serializers import MovieSerializer
from .models import Movie

class SingleMovieAPIView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
