from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Quiz, Question, Answer, QuestionType
import random

class QuizSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'owner']
        expandable_fields = {
            'questions': ('quiz.serializers.QuestionSerializer', {'many': True}),
        }

class AnswerPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ['is_correct', 'score', 'match_pair'] 

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ['question', 'created_at', 'updated_at']


class QuestionSerializer(FlexFieldsModelSerializer):
    answers = AnswerSerializer(many=True, write_only=True)
    answers_read = AnswerPublicSerializer(many=True, read_only=True, source='answers')
    shuffled_match_options = serializers.SerializerMethodField()
    shuffled_order_options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        read_only_fields = ['created_at', 'updated_at']
        fields = [
            'id',
            'text',
            'question_type',
            'order',
            'quiz',
            'answers',              # for write (POST)
            'answers_read',         # for read (GET)
            'shuffled_match_options',
            'shuffled_order_options',
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.question_type in ['TEXT', 'BLANK', QuestionType.MATCH, QuestionType.ORDER]:
            rep.pop('answers_read', None)
        if instance.question_type != QuestionType.MATCH:
            rep.pop('shuffled_match_options', None)
        if instance.question_type != QuestionType.ORDER:
            rep.pop('shuffled_order_options', None)
        return rep

    def get_shuffled_match_options(self, obj):
        if obj.question_type == QuestionType.MATCH:
            matches = [
                {"id": str(a.id), "text": a.match_pair}
                for a in obj.answers.all()
                if a.match_pair
            ]
            random.shuffle(matches)
            return matches
        return []

    def get_shuffled_order_options(self, obj):
        if obj.question_type == QuestionType.ORDER:
            options = [
                {"id": str(a.id), "text": a.text}
                for a in obj.answers.all()
            ]
            random.shuffle(options)
            return options
        return []

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question


   

