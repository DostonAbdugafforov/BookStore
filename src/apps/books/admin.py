from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "price", "genre", "available_copies", "created_at")
    search_fields = ("title", "author")
    list_filter = ("author",)
    ordering = ["-created_at"]

