from django.urls import path
from .views import (RegisterUserAPIView, LoginAPIView, LogoutAPIVIew, ForgotPasswordAPIView,
                    ConfirmCodeAndResetPasswordAPIView)

urlpatterns = [
    path('user/register/', RegisterUserAPIView.as_view()),
    path('user/login/', LoginAPIView.as_view()),
    path('user/logout/', LogoutAPIVIew.as_view()),
    path('forgot-password/sending-code/', ForgotPasswordAPIView.as_view()),
    path('forgot-password/confirm-code/', ConfirmCodeAndResetPasswordAPIView.as_view()),
    path('forgot-password/reset-password/', ConfirmCodeAndResetPasswordAPIView.as_view())
]