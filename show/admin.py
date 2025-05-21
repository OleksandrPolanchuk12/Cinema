from django.contrib import admin

from .models import Show, ShowUnit


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['movie', 'hall', 'prices']
    list_filter = ['movie', 'hall']


@admin.register(ShowUnit)
class ShowUnitAdmin(admin.ModelAdmin):
    list_display = ['show', 'showtime']
