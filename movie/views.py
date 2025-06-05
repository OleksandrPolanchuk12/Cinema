from rest_framework.generics import RetrieveAPIView, CreateAPIView
from .serializers import MovieSerializer, LikeSerializer
from .models import Movie, Like
from rest_framework.response import Response
from rest_framework import status


class SingleMovieAPIView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class RatingMovieAPIVIew(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'movie_id': kwargs['movie_id'],
                                                                     'user': request.user})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        new_like = Like.objects.update_or_create(movie=data['movie'], user=request.user, state=data['rating'])

        return Response(status=status.HTTP_200_OK)
