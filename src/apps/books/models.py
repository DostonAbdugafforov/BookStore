from django.db import models
from apps.common.models import BaseModel


class Book(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Kitob nomi", db_index=True)
    author = models.CharField(max_length=150, verbose_name="Muallif", db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (so'm)")
    genre = models.CharField(max_length=100, verbose_name="Janr", db_index=True)
    available_copies = models.PositiveIntegerField(default=1, verbose_name="Mavjud nusxalar")

    class Meta:
        db_table = "books"
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.author}"