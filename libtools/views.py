from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Book, Transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import TransactionForm, BookForm


def home(request):
    return render(request,'libtools/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('books')  # Redirect to Books List upon successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'libtools/login.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully signed up. You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = UserCreationForm()
    return render(request, 'libtools/signup.html', {'form': form})

@login_required
def books_list(request):
    books = Book.objects.all()
    return render(request, 'libtools/bookslist.html', {'books': books})


def logout_view(request):
    logout(request)
    return redirect('home') 


def dashboard(request):
    # Example: Get counts of books and transactions
    book_count = Book.objects.count()
    transaction_count = Transaction.objects.count()
    
    return render(request, 'libtools/dashboard.html', {'book_count': book_count, 'transaction_count': transaction_count})


def transactions_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'libtools/transactions.html', {'transactions': transactions})


def create_transaction(request):
    available_books = Book.objects.filter(status='available')
    users = User.objects.exclude(username='admin')
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # Process the form data and create a new transaction
            book_id = form.cleaned_data['book']
            transaction_type = form.cleaned_data['transaction_type']
            transaction_date = form.cleaned_data['transaction_date']
            user = form.cleaned_data['user']
            book = get_object_or_404(Book, id=book_id.id)
            
            # Create a new transaction
            transaction = Transaction.objects.create(
                book=book,
                transaction_type=transaction_type,
                transaction_date=transaction_date,
                user=user
            )
            
            # Update book status based on transaction type
            if transaction_type == 'issued':
                book.status = 'issued'
            elif transaction_type == 'returned':
                book.status = 'available'
            book.save()
            
            # Add success message
            messages.success(request, 'Transaction created successfully.')
            
            # Redirect to a success page or another URL
            return redirect('transactions')
        else:
            print("**********",form.errors.items())
            # Add error message if form is invalid
            messages.error(request, 'Failed to create transaction. Please check the form data.')
    else:
        form = TransactionForm()
    return render(request, 'libtools/create_transaction.html', {'form': form,'books':available_books, 'users':users})


def delete_transaction(request, pk):
    # Get the transaction object or return 404 if not found
    transaction = get_object_or_404(Transaction, pk=pk)
    
    transaction.delete()
    
    return redirect('transactions')


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully.')
            return redirect('books')
        else:
            messages.error(request, 'Failed to add book. Please check the form data.')
    else:
        form = BookForm()
    
    return render(request, 'libtools/create_book.html', {'form': form})