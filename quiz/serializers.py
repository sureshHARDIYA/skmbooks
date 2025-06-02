from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Quiz, Question, Answer, QuestionType
import random

class QuizSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        expandable_fields = {
            'questions': ('quiz.serializers.QuestionSerializer', {'many': True}),
        }

class AnswerPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ['is_correct', 'score', 'match_pair'] 

class QuestionSerializer(FlexFieldsModelSerializer):
    answers = AnswerPublicSerializer(many=True, read_only=True)
    shuffled_match_options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        read_only_fields = ['created_at', 'updated_at']
        fields = [
            'id',
            'text',
            'question_type',
            'order',
            'answers',
            'shuffled_match_options'  # Include the field
        ]

        expandable_fields = {
            'answers': ('quiz.serializers.AnswerPublicSerializer', {'many': True}),
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.question_type in ['TEXT', 'BLANK']:
            rep.pop('answers', None)
        return rep

    def get_shuffled_match_options(self, obj):
        if obj.question_type == QuestionType.MATCH:
            pairs = [a.match_pair for a in obj.answers.all() if a.match_pair]
            random.shuffle(pairs)
            return pairs
        return None
   

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']