from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "price"]


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "price",
            "genre",
            "available_copies",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Narx 0 dan katta bo'lishi kerak."
            )
        return value

    def validate_available_copies(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Nusxalar soni manfiy bo'lishi mumkin emas."
            )
        return value


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "price",
            "genre",
            "available_copies",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Narx 0 dan katta bo'lishi kerak."
            )
        return value

    def validate_available_copies(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Nusxalar soni manfiy bo'lishi mumkin emas."
            )
        return value

    def validate(self, attrs):
        if self.partial and not attrs:
            raise serializers.ValidationError(
                "Yangilash uchun kamida bitta field yuborish kerak."
            )
        return attrs