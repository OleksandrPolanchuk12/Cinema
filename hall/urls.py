from django.urls import path
from .views import SeatReservationAPIView, HallCinemaListAPIView, SingleHallAPIView

urlpatterns = [
    path('cinema/<cinema_id>/halls/list/', HallCinemaListAPIView.as_view(), name='hall-cinema'),
    path('cinema/<cinema_id>/hall/<hall_id>/reserve-seats/', SeatReservationAPIView.as_view(), name='seat-reservation'),
    path('cinema/<cinema_id>/hall/<hall_id>/details/', SingleHallAPIView.as_view(), name='hall-cinema-retrieve'),
]