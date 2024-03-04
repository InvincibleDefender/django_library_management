from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Book(models.Model):
    AVAILABLE = 'available'
    ISSUED = 'issued'

    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (ISSUED, 'Issued'),
    ]

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    cover_image = models.ImageField(upload_to='images/', default='images/default_cover.png', blank=True, null=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=AVAILABLE)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    ISSUED = 'issued'
    RETURNED = 'returned'

    TRANSACTION_CHOICES = [
        (ISSUED, 'Issued'),
        (RETURNED, 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    transaction_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.transaction_type}"