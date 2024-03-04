from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('sign-up/', views.signup, name='sign-up'),
    path('books/', views.books_list, name='books'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/', views.transactions_list, name='transactions'),
    path('create-transaction/', views.create_transaction, name='create-transaction'),
    path('transactions/delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('books/add-book/', views.add_book, name='add_book'),
]