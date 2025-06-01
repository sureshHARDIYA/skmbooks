from django.db import models
from books.models import Book
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel  # assuming you've created this

User = get_user_model()

class Quiz(TimeStampedModel):  # gives created_at, updated_at
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quizzes')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.title
