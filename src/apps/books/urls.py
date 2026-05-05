from django.urls import path
from .views import BookDetailView, BookListCreateView

urlpatterns = [
    path("", BookListCreateView.as_view(), name="book-list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book-detail"),
]