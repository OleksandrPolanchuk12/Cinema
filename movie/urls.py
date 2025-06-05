from django.urls import path
from .views import SingleMovieAPIView, RatingMovieAPIVIew

urlpatterns = [
    path('movie/<int:pk>', SingleMovieAPIView.as_view()),
    path('movie/<movie_id>/rating/', RatingMovieAPIVIew.as_view())
]