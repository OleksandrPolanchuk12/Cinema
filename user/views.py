import random

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (UserSerializer, ForgotPasswordSerializer, ConfirmCodeAndResetPasswordSerializer,
                          LoginSerializer)
from .tasks import send_email


class RegisterUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token = Token.objects.create(user=user)

        response = Response({'message': 'Registered successful'}, status=status.HTTP_201_CREATED)
        response['Authorization'] = f'Token {token.key}'
        return response


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = Token.objects.create(user=serializer.validated_data['user'])
        token.save()

        response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        response['Authorization'] = f'Token {token.key}'
        return response


class LogoutAPIVIew(APIView):
    def post(self, request):
        token = request.auth
        if token:
            token.delete()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid token ot not authenticated'}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = random.randint(100000, 999999)
        send_email.delay(email, code)
        request.session["code"] = str(code)
        return Response({'message': 'The letter was sent successfully'}, status=status.HTTP_200_OK)


class ConfirmCodeAndResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(request_body=ConfirmCodeAndResetPasswordSerializer)
    def post(self, request):
        serializer = ConfirmCodeAndResetPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if not (data['email'] and data['new_password'] and data['confirm_new_password']):
            del request.session["code"]
            request.session["code_checked"] = True
            return Response({'message': 'Code confirmed'}, status=status.HTTP_200_OK)

        user = get_object_or_404(User, email=data['email'])
        user.set_password(data['new_password'])
        user.save()

        del request.session["code_checked"]
        return Response({'message': 'Password changed'}, status=status.HTTP_200_OK)
