from django.urls import path
from .views import CinemaListAPIView

urlpatterns = [
    path('cinema/list/',CinemaListAPIView.as_view(), name='cinema-list'),
]