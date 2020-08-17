from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance, Language

# Register your models here.
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Language)