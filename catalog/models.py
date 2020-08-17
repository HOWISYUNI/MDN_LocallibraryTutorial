from django.db import models
import uuid # BookInstance 모델 클래스에서 사용

# Create your models here.

class Genre(models.Model):
    """Model representing a book genre."""
    
    # Field
    name = models.CharField(max_length=200, help_text='Enter a book genre')

    # Methods
    def __str__(self):
        """String for representing the Model object.
            name을 반환하기위한 메서드"""
        return self.name

class Book(models.Model):
    """ Model representing a book. not a specific copy of book """
    
    # Fields
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

        # 관계 : 1. 다대다(ManyToManyField) 2. 일대다(ForeignKey) 3. 일대일(OneToOneField)
    """ 관계
    1. 판단 : 관계를 정할때는 문장으로 만들어서 판단한다.
    : A 하나에 B ~개 필요
      B 하나에 A *개 필요
      -> A : B = ~ : * = ~ 대 * 관계
    2. 선언
      many to many : 둘 중 아무데나
      일 대  ~: '일' 쪽에 Foreignkey 선언"""
    genre = models.ManyToManyField(Genre,help_text='Select a genre for this book')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True) 
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    # Methods
    def __str__(self):
        """String for representing the Model object"""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book.
            모델의 세부 레코드에 접근.
            URL을 통해 특정 레코드의 id가 전송된다면, 응답과 id를 뷰(book detail view)에 전달하기위해 book-detail URL맵퍼를 정의해야한다. 관련 뷰와 템플릿도 정의해야한다. 알맞은 형식의 URL맵퍼를 만들기 위해 reverse()함수를 사용"""
        return revese('book-detail',args=[str(self.id)])

class BookInstance(models.Model):
    """ Model representing a specific copy of a book
        같은 제목의 책에 대해 서로 다른 고유번호를 할당해서 관리"""

    # Fields
            # 관계
    '''uuid : 식별자(ID, PRIMARY KEY)로 사용할 수 있는 32자리 임의의 식별자. 순차적 ID가 레코드에 할당되는게 싫을때 사용'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book',on_delete=models.SET_NULL, null=True)

    imprint = models.CharField(max_length=200) # 출판사
    due_back = models.DateField(null=True, blank=True)




    ''' status 필드를 위한 LOAN_STATUS 튜플 자료구조. 하드코딩된 선택리스트 
        status의 choices인자에 전달된다.'''
    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    # Metadata : BookInstance 모델 클래스의 설정
    class Meta:
        ordering = ['due_back']

    # Methods
    def __str__(self):
        """String for representing the Model object"""
        return f'{self.id} ({self.book.title})' # python string조작은 f-string이 갑이다

class Author(models.Model):
    """Model representing an author"""

    # Fields
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    # Metadata
    class Meta:
        ordering = ['last_name','first_name']

    # Methos
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])
    def __str__(self):
        """ String for representing the Model object"""
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    """Model representing an language"""

    # Fields
    name = models.CharField(max_length = 200,help_text="Enter the book's language(eg.English, French etc...)")

    # Metadata
    class Meta:
        ordering = ['name']

    # Methods
    def __str__(self):
        return self.name # sring 1개 처리는 굳이 f-string을 사용할 필요 없습니다.
