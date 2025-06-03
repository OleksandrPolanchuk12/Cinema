from django.urls import path
from .views import SingleMovieAPIView

urlpatterns = [
    path('movie/<int:pk>', SingleMovieAPIView.as_view())
]