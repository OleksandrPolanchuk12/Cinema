from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(validated_data.password)
        user.save()
        return user
