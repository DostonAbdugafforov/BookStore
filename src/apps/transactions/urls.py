from django.urls import path
from .views import BuyBookView, MyTransactionsView, RentBookView

urlpatterns = [
    path("buy/<int:book_id>/", BuyBookView.as_view(), name="buy-book"),
    path("rent/<int:book_id>/", RentBookView.as_view(), name="rent-book"),
    path("my/transactions/", MyTransactionsView.as_view(), name="my-transactions"),
]