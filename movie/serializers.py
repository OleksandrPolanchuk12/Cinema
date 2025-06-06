from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import Movie, Like
from django.shortcuts import get_object_or_404

class MovieSerializer(ModelSerializer):
    rating_user = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = '__all__'

    def get_rating_user(self, obj):
        request = self.context.get('request')
        if request:
            like = Like.objects.filter(user=request.user, movie=obj).first()
            return like.state if like else None
        return None

class LikeSerializer(Serializer):
    rating = serializers.BooleanField()

    def validate(self, data):
        movie = get_object_or_404(Movie, id=self.context.get('movie_id'))
        rating = data.get('rating')

        like = Like.objects.filter(movie=movie, user=self.context.get('user')).first()
        if like:
            if like.state == rating:
                raise serializers.ValidationError({'message': 'Like with same state already exists'})
            movie.rating += 2 if rating else -2
            movie.save()
            like.delete()

        if not like:
            movie.rating += 1 if rating else -1
            movie.save()
        data['movie'] = movie
        return data