import uuid
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Quiz
from .serializers import QuizSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_object(self):
        lookup_value = self.kwargs.get('pk')  # or 'slug' depending on URL conf
        try:
            uuid_val = uuid.UUID(lookup_value, version=4)
            condition = Q(id=uuid_val)
        except ValueError:
            condition = Q(slug=lookup_value)
        return get_object_or_404(self.get_queryset(), condition)