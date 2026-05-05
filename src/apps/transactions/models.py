from django.conf import settings
from django.db import models
from apps.common.models import BaseModel


class Transaction(BaseModel):
    class TransactionType(models.TextChoices):
        BUY = "buy", "Sotib olish"
        RENT = "rent", "Ijaraga olish"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="Foydalanuvchi",
    )
    book = models.ForeignKey(
        "books.Book",
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="Kitob",
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        verbose_name="Tur",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="To'lov summasi"
    )

    class Meta:
        db_table = "transactions"
        verbose_name = "Tranzaksiya"
        verbose_name_plural = "Tranzaksiyalar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} | {self.get_transaction_type_display()} | {self.book}"