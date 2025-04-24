from django.urls import path
from .views import CinemaListView

urlpatterns = [
    path('cinemas/',CinemaListView.as_view(), name='cinema_list'),
]