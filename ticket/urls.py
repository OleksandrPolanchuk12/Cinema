from django.urls import path
from .views import SeatReservationAPIView, TicketListAPIView

urlpatterns = [
    path('cinema/<cinema_id>/show_unit/<show_id>/reserve-seats/', SeatReservationAPIView.as_view(),
         name='seat-reservation'),
    path('reserved-seats/user/<user_id>/', TicketListAPIView.as_view())
]