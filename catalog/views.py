import datetime

from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView # Generic Edit View 사용하기
from django.contrib.auth.mixins import LoginRequiredMixin # 로그인된 유저만 접근하는 view 생성
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required # 권한부여를 데코레이터(decorator)를 사용해 부여

from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm

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
    num_visits = request.session.get('num_visits',0) #방문한적이 없다면 0으로 초기화한다.
    """ 복잡한 현재 세션 id를 직접입력하지않고 'num_visits'키값에 맵핑해 쉽게접근하도록 구성. 세션id당 어떤 값을 저장할 수 있도록 설계.
        세션 아이디와 그에 대한 값들은 DB에 저장된다.
        request.session['num_visits']  = 값: 'num_visits'키값에 맵핑돼있는 세션 id가 어떤 값을 가질 수 있다.
        request.session.get('num_visits',0) : 'num_visits'키값에 맵핑돼있는 세션id 에 저장된 값을 가져온다."""
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_visits' : num_visits,
    }

    # Render HTML template index.html with the data in the contxt variable
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

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    # queryset이 아닌 get_queryset 메서드 오버라이딩한 ORM 표현방식
    def get_queryset(self):
        # 빌린책(status__exact = 'o') 중 로그인한 유저가 빌린(borrower = self.request.user) 데이터. due_back순으로 정렬
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

# # CBV 형식으로 작성한 대출된 책 뷰
# class AllLoanedBookListView(generic.ListView):
#     model = BookInstance
#     template_name = 'catalog/bookinstance_list_borrowed_all.html'
#     paginate_by = 10

#     def get_queryset(self):
#         return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.staff_member_required')
def all_loaned_book_list_view(request):
    loaned_book_list = BookInstance.objects.all()
    context = {'bookinstance_list' : loaned_book_list}
    return render(request, 'catalog/bookinstance_list_borrowed_all.html', context)


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    # pk에 해당하는 특정 객체를 반환하거나 없으면 404 예외를 발생
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # POST 요청이면 폼 데이터 바인딩(binding)
    if request.method == 'POST':

        # form 인스턴스 생성 + 바인딩(binding, 제출할 데이터를 채운다)
        book_renewal_form = RenewBookForm(request.POST)

        # form 유효성체크
        if book_renewal_form.is_valid():
            # 사전타입 form.cleand_data 를 due_back필드에 넣는다.
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.save() # db갱신

            # 데이터 갱신 성공 후 이동할 특정URL로 보낸다.
            return HttpResponseRedirect(reverse('all-borrowed'))

    # POST 이외의 요청(ex.GET)이면 기본 폼 생성
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date' : proposed_renewal_date})

    context = {
        'form' : book_renewal_form,
        'book_instance' : book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html',context)

# Generic Edit View를 사용하는 아래 세가지 클래스. 
# Edit View를 사용하면 post, get 메서드를 귀찮게 구분하지 않아도 알아서 처리해준다.
# modelForm까지 자동으로 만들어준다.
# Create, Update : <model_name>_form.html 의 템플릿을 같이쓴다.
# Delete : <model_name>_confirm_delete.html 템플릿을 쓴다.
# 두 템플릿의 suffix(_form, _confirm_delete 은 클래스 안에서 template_name_suffix 인자로 변경할 수 있다.)
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__' # Author 모델의 모든 필드를 가져온다.
    initial = {'date_of_death' : '05/01/2018',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = {'first_name', 'last_name', 'date_of_birth', 'date_of_death'}

class AuthorDelete(Deleteview):
    model = Author
    success_url = reverse_lazy('authors') # Delete 성공시 redirect되는 url, urls.py에서 name='authors'를 찾아간다.