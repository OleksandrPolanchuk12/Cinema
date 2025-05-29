from django.contrib.auth import authenticate
from django.template.context_processors import request
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4)
    confirm_password = serializers.CharField(min_length=4)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'error': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(f'Email {email} does not exist')
        return data


class ConfirmCodeAndResetPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(allow_blank=True, allow_null=True)
    email = serializers.EmailField(allow_blank=True, allow_null=True)
    new_password = serializers.CharField(allow_blank=True, allow_null=True)
    confirm_new_password = serializers.CharField(allow_blank=True, allow_null=True)

    def validate(self, data):
        request = self.context.get('request')
        code = data.get('code')
        email = data.get('email')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if code:
            correct_code = request.session.get("code")
            if not correct_code:
                raise serializers.ValidationError({'code': 'No code found or expired in session'})
            if str(code) != str(correct_code):
                raise serializers.ValidationError({'code': 'Wrong code'})

        if not (email and new_password and confirm_new_password):
            return data

        if not request.session.get("code_checked"):
            raise serializers.ValidationError({'message': 'Code not confirmed'})

        if new_password != confirm_new_password:
            raise serializers.ValidationError({'message': 'Passwords do not match'})

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(f'Email {email} does not exist')

        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError({'Email and password are required'})

        user = authenticate(request, email=email, password=password)
        data['user'] = user

        if not user:
            raise serializers.ValidationError({'Invalid email pr password'})

        return data
