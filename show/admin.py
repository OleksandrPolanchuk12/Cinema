from django.contrib import admin
from .models import Show

@admin.register(Show)
class ShowAdmin(admin.ModdelAdmin):
    list_display = ('movie', 'hall', 'start_data', 'end_data')
    list_filter = ('movie', 'hall')