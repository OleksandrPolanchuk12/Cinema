from rest_framework.serializers import ModelSerializer

from .models import Show, ShowUnit


class ShowSerializer(ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'hall', 'movie', 'prices']

class ShowUnitSerializer(ModelSerializer):
    class Meta:
        model = ShowUnit
        fields = ['show', 'showtime']