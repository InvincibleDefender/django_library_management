from django import forms
from .models import Transaction, Book

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['book', 'transaction_type', 'user', 'transaction_date']

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn', 'cover_image', 'description']