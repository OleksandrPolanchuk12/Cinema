from django.urls import path
from .views import (RegisterUserAPIView, LoginAPIView, LogoutAPIVIew, ForgotPasswordAPIView, ConfirmCodeAPIView,
                    ResetPasswordAPIView)

urlpatterns = [
    path('register-user/', RegisterUserAPIView.as_view()),
    path('login-user/', LoginAPIView.as_view()),
    path('logout-user/', LogoutAPIVIew.as_view()),
    path('forgot-password/', ForgotPasswordAPIView.as_view()),
    path('confirm-code/', ConfirmCodeAPIView.as_view()),
    path('reset-password/', ResetPasswordAPIView.as_view())
]