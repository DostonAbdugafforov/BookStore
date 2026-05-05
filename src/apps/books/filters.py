import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(lookup_expr="icontains", label="Janr")
    author = django_filters.CharFilter(lookup_expr="icontains", label="Muallif")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ["genre", "author", "min_price", "max_price"]