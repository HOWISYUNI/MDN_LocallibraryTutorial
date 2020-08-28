from django.urls import path
from catalog import views

urlpatterns = [
    path('',views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBookByUserListView.as_view(), name = 'my-borrowed'),
    # path('books/borrowed',views.AllLoanedBookListView.as_view(), name='all-borrowed'),
    path('books/borrowed',views.all_loaned_book_list_view, name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]