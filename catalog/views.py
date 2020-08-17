from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

# Create your views here.

"""Function-Based View(FBV) : 전통적인 방식"""
def index(request):
    """View function for home page of site"""

    # count main object
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (Status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count() # status__exact : 'status'중에서 정확히(exact) 상태가 a인 것을 골라라. SQL의 WHERE문으로 변환된다.https://docs.djangoproject.com/en/3.0/topics/db/queries/  2. dunder(double underbar) 주의 : status_exact가 아니라 status__exact임.

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variables.
    # 현재 유저가 index페이지를 몇 번 방문했는지 출력
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_author' : num_author,
        'num_visits' : num_visits,
    }

    # Render the HTML template index.html with the data in the contxt variable
    return render(request, 'index.html', context=context)

"""Class-Based View(CBV)"""
class BookListView(generic.ListView):
    """django에서 기본 제공되는 class - based generic LIST view"""
    """ Generic views는 /application_name/templates 디렉터리 아래의 /application_name/[the_model_name]_list.html 에서 자동으로 템플릿을 찾는다.
        이 예시에서는 catalog/templates 디렉터리 아래의 /catalog/book_list.html 에서 템플릿을 찾는다."""
    model = Book

    # 페이지네이션(Pagination). 한 페이지당 book 10개만 보여준다.
    paginate_by = 10

    # 다른 속성이나 디폴트동작들을 추가할 수 있다. 자세한내용은 MDN Django tutorial part 6 참고

class BookDetailView(generic.DetailView):
    """django에서 기본 제공되는 class - based generic DETAIL view"""
    model = Book

