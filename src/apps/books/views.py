import logging

from django.core.cache import cache
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import BookFilter
from .models import Book
from .serializers import BookCreateSerializer, BookSerializer, BookDetailSerializer
from apps.users.permissions import IsAdmin

logger = logging.getLogger("apps.books")

BOOK_CACHE_KEY = "book:{id}"


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    filterset_class = BookFilter
    search_fields = ["title", "author", "genre"]
    ordering_fields = ["price", "created_at", "title"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookCreateSerializer
        return BookSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        book = serializer.save()
        logger.info(
            f"Yangi kitob: '{book.title}' "
            f"(sotuvchi: {self.request.user.email})"
        )


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        book_id = kwargs["pk"]
        cache_key = BOOK_CACHE_KEY.format(id=book_id)

        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Kitob #{book_id} keshdan qaytarildi.")
            return Response(cached_data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        cache.set(cache_key, data, timeout=settings.BOOK_CACHE_TTL)
        logger.info(f"Kitob #{book_id} keshga saqlandi.")
        return Response(data)

    def perform_update(self, serializer):
        book = serializer.save()
        cache.delete(BOOK_CACHE_KEY.format(id=book.id))
        logger.info(f"Kitob yangilandi: '{book.title}' (ID={book.id})")

    def perform_destroy(self, instance):
        cache.delete(BOOK_CACHE_KEY.format(id=instance.id))
        logger.info(f"Kitob o'chirildi: '{instance.title}' (ID={instance.id})")
        instance.delete()