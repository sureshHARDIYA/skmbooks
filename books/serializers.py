from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Book
from quiz.serializers import QuizSerializer

class BookSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'owner']
        expandable_fields = {
            'quizzes': ('quiz.serializers.QuizSerializer', {'many': True}),
        }
