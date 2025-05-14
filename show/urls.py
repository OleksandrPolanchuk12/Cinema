from django.urls import path
from .views import CurrentDayShowAPIView, ShowDetailAPIView

urlpatterns = [
    path('cinema/<cinema_id>/shows/', CurrentDayShowAPIView.as_view()),
    path('cinema/<cinema_id>/show/<int:pk>/detail', ShowDetailAPIView.as_view())
]
