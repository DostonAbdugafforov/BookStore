from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "role", 'balance', 'password', "is_active", "is_staff")
    list_filter = ("role", "is_active")
    search_fields = ("email", "name")
    ordering = ("-id",)