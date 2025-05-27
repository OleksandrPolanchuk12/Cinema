from django.urls import path
from .views import (RegisterUserAPIView, LoginAPIView, LogoutAPIVIew, ForgotPasswordAPIView,
                    ConfirmCodeAndResetPasswordAPIView)

urlpatterns = [
    path('register-user/', RegisterUserAPIView.as_view()),
    path('login-user/', LoginAPIView.as_view()),
    path('logout-user/', LogoutAPIVIew.as_view()),
    path('forgot-password/', ForgotPasswordAPIView.as_view()),
    path('confirm-code/', ConfirmCodeAndResetPasswordAPIView.as_view()),
    path('reset-password/', ConfirmCodeAndResetPasswordAPIView.as_view())
]