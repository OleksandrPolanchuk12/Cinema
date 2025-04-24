from rest_framework.serializers import ModelSerializer
from .models import Cinema

class CinemaSerializer(ModelSerializer):
    class Meta:
        model = Cinema
        fields = ['name', 'address', 'phone', 'email', 'city']