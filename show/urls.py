from django.urls import path
from .views import CurrentDayShowAPIView

urlpatterns = [
    path('cinema/<cinema_id>/shows/', CurrentDayShowAPIView.as_view())
]
