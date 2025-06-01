from rest_framework import serializers
from .models import Quiz, Question, Answer

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

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