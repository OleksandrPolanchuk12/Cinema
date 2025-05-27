import random

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer
from .tasks import send_email


class RegisterUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

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

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'message': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({'message': 'Invalid email pr password'}, status=status.HTTP_400_BAD_REQUEST)

        token = Token.objects.create(user=user)
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

    def post(self, request):
        email = request.data.get('email')
        if not User.objects.filter(email=email).exists():
            return Response({'message': f'Email {email} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        code = random.randint(100000, 999999)
        send_email.delay(email, code)
        request.session["code"] = str(code)
        return Response({'message': 'The letter was sent successfully'}, status=status.HTTP_200_OK)


class ConfirmCodeAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        code = request.data.get('code')
        correct_code = request.session.get("code")
        if str(code) != correct_code:
            return Response({'message': 'Wrong code'}, status=status.HTTP_400_BAD_REQUEST)
        del request.session["code"]
        request.session["code_checked"] = True
        return Response({'message': 'Code confirmed'}, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        if not request.session.get("code_checked"):
            return Response({'message': 'Code not confirmed'}, status=status.HTTP_403_FORBIDDEN)
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')
        if new_password != confirm_new_password:
            return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, email=email)
        user.set_password(new_password)
        user.save()

        del request.session["code_checked"]
        return Response({'message': 'Password changed'}, status=status.HTTP_200_OK)
