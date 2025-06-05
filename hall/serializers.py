from rest_framework.serializers import ModelSerializer

from .models import Hall


class HallSerializer(ModelSerializer):
    class Meta:
        model = Hall
        fields = ['id', 'name', 'capacity', 'row', 'seat', 'cinema']
