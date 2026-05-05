from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id", "user_email", "book_title",
            "transaction_type", "amount", "created_at",
        ]
        read_only_fields = fields


class BuyResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    transaction = TransactionSerializer()
    remaining_balance = serializers.DecimalField(max_digits=12, decimal_places=2)