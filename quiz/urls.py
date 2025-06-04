from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuestionViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')      # ✅ Fix here
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')

app_name = 'quiz'
urlpatterns = router.urls
