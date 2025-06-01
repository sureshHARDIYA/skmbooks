from django.contrib import admin
from .models import Book

# Register your models here.

class BookAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ["title"]}
  list_display = ("title", "published_date", "isbn", "pages", "publisher", "published_year")
  search_fields = ("title", "isbn")
  

admin.site.register(Book, BookAdmin)