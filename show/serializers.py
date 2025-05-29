from rest_framework.serializers import ModelSerializer
from rest_framework import  serializers
from datetime import  datetime

from .models import Show, ShowUnit


class ShowSerializer(ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'hall', 'movie', 'prices']


class ShowUnitSerializer(ModelSerializer):
    class Meta:
        model = ShowUnit
        fields = ['show', 'showtime']


class CurrentShowDaySerializer(serializers.Serializer):
    show_start_data = serializers.DateTimeField()
    show_end_data = serializers.DateTimeField()

    def validate(self, data):
        show_start_data = data.get('show_start_data')
        show_end_data = data.get('show_end_data')

        if not show_start_data:
            raise serializers.ValidationError({'message': 'Missing show_start parameter'})
        try:
            data['show_start'] = datetime.fromisoformat(show_start_data)
        except ValueError:
            raise serializers.ValidationError({'message': 'Invalid datetime format'})

        try:
            data['show_end'] = show_end_data and datetime.fromisoformat(show_end_data)
        except ValueError:
            return serializers.ValidationError({'message': 'Invalid datetime format'})

        return data