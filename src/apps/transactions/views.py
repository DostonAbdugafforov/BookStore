import logging
from decimal import Decimal

from django.core.cache import cache
from django.db import transaction as db_transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.books.models import Book
from .models import Transaction
from .serializers import BuyResponseSerializer, TransactionSerializer

logger = logging.getLogger("apps.transactions")

RENT_RATIO = Decimal("0.20")
BOOK_CACHE_KEY = "book:{id}"


def _process_transaction(user, book_id, transaction_type):
    """
    Asosiy biznes logika.
    select_for_update() — bir vaqtda bir nechta so'rovda muammo bo'lmasin.
    """
    with db_transaction.atomic():
        # Kitobni qulflash
        try:
            book = Book.objects.select_for_update().get(id=book_id)
        except Book.DoesNotExist:
            return None, f"Kitob (ID={book_id}) topilmadi.", status.HTTP_404_NOT_FOUND

        # Nusxalar tekshiruvi
        if book.available_copies < 1:
            return None, "Bu kitobning mavjud nusxasi qolmagan.", status.HTTP_409_CONFLICT

        # Narx hisoblash
        if transaction_type == Transaction.TransactionType.BUY:
            amount = book.price
        else:
            amount = (book.price * RENT_RATIO).quantize(Decimal("0.01"))

        # Balans tekshiruvi
        if user.balance < amount:
            return (
                None,
                f"Balans yetarli emas. Kerak: {amount} so'm, mavjud: {user.balance} so'm.",
                status.HTTP_402_PAYMENT_REQUIRED,
            )

        # Amallarni bajarish
        user.balance -= amount
        book.available_copies -= 1
        user.save(update_fields=["balance"])
        book.save(update_fields=["available_copies"])

        txn = Transaction.objects.create(
            user=user,
            book=book,
            transaction_type=transaction_type,
            amount=amount,
        )

        # Redis keshni tozalash
        cache.delete(BOOK_CACHE_KEY.format(id=book_id))

        action = "sotib olindi" if transaction_type == Transaction.TransactionType.BUY else "ijaraga olindi"
        logger.info(
            f"Tranzaksiya: user={user.email} '{book.title}' {action} "
            f"({amount} so'm). Qolgan balans: {user.balance}"
        )

        result = {
            "message": f"'{book.title}' muvaffaqiyatli {action}!",
            "transaction": txn,
            "remaining_balance": user.balance,
        }
        return result, None, None


class BuyBookView(APIView):
    """POST /buy/{book_id}/ — Kitobni sotib olish"""
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        result, error, error_status = _process_transaction(
            user=request.user,
            book_id=book_id,
            transaction_type=Transaction.TransactionType.BUY,
        )
        if error:
            return Response({"detail": error}, status=error_status)

        serializer = BuyResponseSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RentBookView(APIView):
    """POST /rent/{book_id}/ — Kitobni ijaraga olish (narxning 20%)"""
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        result, error, error_status = _process_transaction(
            user=request.user,
            book_id=book_id,
            transaction_type=Transaction.TransactionType.RENT,
        )
        if error:
            return Response({"detail": error}, status=error_status)

        serializer = BuyResponseSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyTransactionsView(generics.ListAPIView):
    """GET /my/transactions/ — Shaxsiy tranzaksiyalar tarixi"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related("book", "user")