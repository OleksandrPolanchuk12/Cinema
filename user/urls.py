from django.urls import path
from .views import RegisterUserAPIView, LoginAPIView, LogoutAPIVIew

urlpatterns = [
    path('register-user/', RegisterUserAPIView.as_view()),
    path('login-user/', LoginAPIView.as_view()),
    path('logout-user/', LogoutAPIVIew.as_view())
]