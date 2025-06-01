from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Quiz, Question, Answer

class QuizSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        expandable_fields = {
            'questions': ('quiz.serializers.QuestionSerializer', {'many': True}),
        }

class QuestionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        expandable_fields = {
            'answers': ('quiz.serializers.AnswerSerializer', {'many': True}),
        }

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            if instance.question_type in ['TEXT', 'BLANK']:
                rep.pop('answers', None)  # hide answers for free text or blanks
            return rep

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']