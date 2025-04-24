from django.urls import path
from .views import SeatReservationView, HallCinemaView

urlpatterns = [
    path('cinema/<cinema_id>/hall/', HallCinemaView.as_view(), name='hall_cinema'),
    path('cinema/<cinema_id>/hall/<hall_id>/', SeatReservationView.as_view(), name='seat_reservation'),
]