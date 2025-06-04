import uuid
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Q

from .models import Quiz, Question, Answer, UserQuizSession, UserAnswer
from .serializers import QuizSerializer
from .utils import check_answer  # Helper function to evaluate answers
from gamification.services import award_points_and_check_badges


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get_object(self):
        lookup_value = self.kwargs.get('pk')
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
        is_correct, awarded_score, correct_ids, feedback = check_answer(question, response)

        return Response({
            "is_correct": is_correct,
            "score_awarded": awarded_score,
            "correct_answer_ids": correct_ids if correct_ids else None,
            "feedback": feedback
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="test/submit")
    def submit_test(self, request):
        user = request.user
        quiz_id = request.data.get("quiz_id")
        answers_data = request.data.get("answers", [])

        quiz = get_object_or_404(Quiz, id=quiz_id)
        session, created = UserQuizSession.objects.get_or_create(
            user=user, quiz=quiz, defaults={"started_at": timezone.now()}
        )

        if session.is_completed:
            return Response({"detail": "Quiz already completed."}, status=400)

        total_score = 0

        for item in answers_data:
            question_id = item["question_id"]
            response = item["response"]
            question = get_object_or_404(Question, id=question_id, quiz=quiz)

            is_correct, score, _, _ = check_answer(question, response)

            UserAnswer.objects.create(
                session=session,
                question=question,
                selected_answer_ids=response,
                is_correct=is_correct,
                score=score
            )
            total_score += score

        session.score = total_score
        session.completed_at = timezone.now()
        session.is_completed = True
        session.save()

        # Gamification hook
        profile = user.profile
        profile.quizzes_completed += 1
        profile.save()
        award_points_and_check_badges(profile, points=total_score, reason=f"Completed quiz: {quiz.title}")

        return Response({
            "quiz_id": quiz.id,
            "total_score": total_score,
            "completed": True
        })
