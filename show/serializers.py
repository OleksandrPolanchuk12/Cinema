from rest_framework.serializers import ModelSerializer
from .models import Show

class ShowSerializer(ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'hall', 'movie', 'showtime', 'prices']