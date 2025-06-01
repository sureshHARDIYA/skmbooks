from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookListView(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('created_at')
    serializer_class = BookSerializer
