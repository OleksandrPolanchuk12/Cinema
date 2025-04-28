from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'age_restrictions', 'director', 'genres', 'release_date', 'duration', 'poster']
    search_fields = ['title',]
