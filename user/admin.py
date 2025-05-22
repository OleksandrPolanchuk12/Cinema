from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ['email']
    list_display = ['email', 'is_staff', 'is_superuser']
