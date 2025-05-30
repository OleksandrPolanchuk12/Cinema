from rest_framework.serializers import ModelSerializer
from rest_framework import  serializers
from datetime import  datetime

from .models import Show, ShowUnit


class ShowSerializer(ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'hall', 'movie', 'prices', 'start_show', 'end_show']


class ShowUnitSerializer(ModelSerializer):
    class Meta:
        model = ShowUnit
        fields = ['show', 'showtime']


class CurrentShowDaySerializer(serializers.Serializer):
    show_start_data = serializers.DateTimeField()
    show_end_data = serializers.DateTimeField()
