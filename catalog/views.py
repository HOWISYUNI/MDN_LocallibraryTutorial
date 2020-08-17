from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
    """View function for home page of site"""

    # count main object
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (Status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count() # status__exact : 'status'중에서 정확히(exact) 상태가 a인 것을 골라라. SQL의 WHERE문으로 변환된다.https://docs.djangoproject.com/en/3.0/topics/db/queries/  2. dunder(double underbar) 주의 : status_exact가 아니라 status__exact임.

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render HTML template index.html & context variable
    return render(request, 'index.html', context=context)