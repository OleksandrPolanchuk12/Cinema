import random

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


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
        user.set_password(password)
        user.save()

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


