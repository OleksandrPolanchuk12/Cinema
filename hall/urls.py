from django.urls import path
from .views import SeatReservationAPIView, HallCinemaAPIView

urlpatterns = [
    path('cinema/<cinema_id>/hall/', HallCinemaAPIView.as_view(), name='hall-cinema'),
    path('cinema/<cinema_id>/hall/<hall_id>/', SeatReservationAPIView.as_view(), name='seat-reservation'),
]