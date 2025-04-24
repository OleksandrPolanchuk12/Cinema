from django.contrib import admin
from .models import Cinema

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone', 'email']
    search_fields = ['name', 'address']
    list_filter = ['name']
