from django.urls import path
from .views import CurrentDayShowAPIView

urlpatterns = [
    path('cinema/<cinema_id>/show/today/', CurrentDayShowAPIView.as_view())        
]
