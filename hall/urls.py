from django.urls import path

from .views import HallCinemaListAPIView, SingleHallAPIView

urlpatterns = [
    path('cinema/<cinema_id>/halls/list/', HallCinemaListAPIView.as_view(), name='hall-cinema'),
    path('cinema/<cinema_id>/hall/<hall_id>/details/', SingleHallAPIView.as_view(), name='hall-cinema-retrieve'),
]
