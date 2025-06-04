from django.urls import path
from .views import SeatReservationAPIView, TicketListAPIView, FreeSeatsAPIView

urlpatterns = [
    path('cinema/<cinema_id>/show_unit/<show_id>/reserve-seats/', SeatReservationAPIView.as_view()),
    path('reserved-seats/user/<user_id>/', TicketListAPIView.as_view()),
    path('cinema/<cinema_id>/hall/<hall_id>/show_unit/<show_unit_id>/free-seats/', FreeSeatsAPIView.as_view())
]