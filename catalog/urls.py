from django.urls import path
from catalog import views

urlpatterns = [
    path('',views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<uuid:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('mybooks/', views.LoanedBookByUserListView.as_view(), name = 'my-borrowed'),
    path('books/borrowed',AllLoanedBookListView.as_view(), name='all-borrowed')
]