from django.urls import path
from .views import CinemaListAPIView

urlpatterns = [
    path('cinemas/',CinemaListAPIView.as_view(), name='cinema-list'),
]