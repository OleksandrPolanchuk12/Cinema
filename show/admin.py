from django.contrib import admin
from .models import Show

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['movie', 'hall', 'showtimes', 'prices']
    list_filter = ['movie', 'hall']