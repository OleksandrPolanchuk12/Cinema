from django.urls import path
from .views import SeatReservationAPIView, HallCinemaListAPIView, SingleHallAPIView

urlpatterns = [
    path('cinema/<cinema_id>/hall/', HallCinemaListAPIView.as_view(), name='hall-cinema'),
    path('cinema/<cinema_id>/hall/<hall_id>/', SeatReservationAPIView.as_view(), name='seat-reservation'),
    path('cinema/<cinema_id>/hall/<hall_id>', SingleHallAPIView.as_view(), name='hall-cinema-retrieve'),
]