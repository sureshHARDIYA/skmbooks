import uuid
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .models import Quiz, Question, QuestionType, Answer
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
    
    @action(detail=False, methods=["post"], url_path="practice/answer")
    def check_practice_answer(self, request):
        question_id = request.data.get("question_id")
        response = request.data.get("response")

        question = get_object_or_404(Question, id=question_id)
        is_correct = False
        awarded_score = 0
        feedback = []
        correct_ids = list(
            question.answers.filter(is_correct=True).values_list("id", flat=True)
        )

        if question.question_type == QuestionType.SINGLE_CHOICE:
            selected_answer = Answer.objects.filter(id=response[0], question=question).first()
            if selected_answer:
                question = question.text
                selected_answer = selected_answer
                is_correct = selected_answer.is_correct
                awarded_score = selected_answer.score if is_correct else 0
                feedback_text = (
                    selected_answer.feedback_if_correct if is_correct else selected_answer.feedback_if_wrong
                )
                feedback.append(feedback_text)

        elif question.question_type == QuestionType.MULTI_SELECT:
            selected_answers = Answer.objects.filter(id__in=response, question=question)
            selected_ids = [str(ans.id) for ans in selected_answers]
            is_correct = sorted(selected_ids) == sorted([str(cid) for cid in correct_ids])
            awarded_score = sum(a.score for a in selected_answers if a.id in correct_ids)

            for ans in selected_answers:
                fb = ans.feedback_if_correct if ans.is_correct else ans.feedback_if_wrong
                if fb:
                    feedback.append(fb)

        elif question.question_type == QuestionType.FREE_TEXT:
            correct_answer = question.answers.first().text.strip().lower()
            is_correct = response.strip().lower() == correct_answer
            awarded_score = question.answers.first().score if is_correct else 0
            feedback_text = (
                question.answers.first().feedback_if_correct if is_correct else question.answers.first().feedback_if_wrong
            )
            if feedback_text:
                feedback.append(feedback_text)

        return Response({
            "is_correct": is_correct,
            "score_awarded": awarded_score,
            "correct_answer_ids": correct_ids if correct_ids else None,
            "feedback": feedback
        }, status=status.HTTP_200_OK)
