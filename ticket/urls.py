from django.urls import path
from .views import SeatReservationAPIView

urlpatterns = [
    path('cinema/<cinema_id>/show_unit/<show_id>/reserve-seats/', SeatReservationAPIView.as_view(), name='seat-reservation')
]