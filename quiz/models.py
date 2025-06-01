from django.db import models
from books.models import Book
from django.contrib.auth import get_user_model
from core.models import BaseModel  
from django.db.models import Max

User = get_user_model()

class QuestionType(models.TextChoices):
    SINGLE_CHOICE = 'SINGLE', 'Single Choice'
    MULTI_SELECT = 'MULTI', 'Multiple Select'
    FREE_TEXT = 'TEXT', 'Free Text'
    FILL_BLANKS = 'BLANK', 'Fill in the Blanks'
    TRUE_FALSE = 'BOOL', 'True/False'
    ORDER = 'ORDER', 'Arrange in Order'
    MATCH = 'MATCH', 'Match the Following'

class Quiz(BaseModel):  
    title = models.CharField(max_length=200)
    slug = models.SlugField(default="", null=False, blank=True, unique=True)
    description = models.TextField(blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quizzes')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.title


class Question(BaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    question_type = models.CharField(max_length=10, choices=QuestionType.choices)


    def __str__(self):
        return f"Question {self.order} for {self.quiz.title}"
    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if self.order == 0:
            last_order = Question.objects.filter(quiz=self.quiz).aggregate(models.Max('order'))['order__max'] or 0
            self.order = last_order + 1
        super().save(*args, **kwargs)

class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    match_pair = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Answer {self.order} for {self.question.text}"

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.order == 0 and self.question:  # ensure question exists
            last_order = Answer.objects.filter(question=self.question).aggregate(
                Max('order')
            )['order__max'] or 0
            self.order = last_order + 1
        super().save(*args, **kwargs)

class UserQuizSession(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
    
class UserAnswer(BaseModel):
    session = models.ForeignKey(UserQuizSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer_ids = models.JSONField()  # UUID list or plain text for free input
    is_correct = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Answer by {self.session.user.username} for {self.question.id}"