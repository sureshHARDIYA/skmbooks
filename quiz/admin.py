from django.contrib import admin
from .models import Quiz, Question, Answer, QuestionType, UserQuizSession, UserAnswer
from django import forms

class AnswerInlineForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10, 'cols': 30}),
            'feedback_if_correct': forms.Textarea(attrs={'rows': 10, 'cols': 30}),
            'feedback_if_wrong': forms.Textarea(attrs={'rows': 10, 'cols': 30}),
        }

class AnswerInline(admin.TabularInline):
    exclude = ['order']
    model = Answer
    form = AnswerInlineForm
    extra = 1
    # fields = ('text', 'is_correct', 'score')
    show_change_link = True
    verbose_name = "Answer"
    verbose_name_plural = "Answers"
    # autocomplete_fields = ['question']

class QuestionInline(admin.TabularInline):
    model = Question
    exclude = ['order']
    extra = 1
    show_change_link = True

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "text", "order", "created_at", "updated_at")
    exclude = ['order']
    inlines = [AnswerInline]

class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "book", "owner", "created_at", "updated_at")
    inlines = [QuestionInline]
    prepopulated_fields = {"slug": ["title"]}

class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "is_correct", "order", "score", "created_at", "updated_at")
    exclude = ['order']

class UserQuizSessionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'quiz',
        'score',
        'is_completed',
        'started_at',
        'completed_at',
    )
    list_filter = ('is_completed', 'quiz')
    search_fields = ('user__username', 'quiz__title')
    ordering = ('-started_at',)

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'session_display',
        'question',
        'is_correct',
        'score',
        'created_at',
        'updated_at',
    )
    search_fields = ('session__user__username', 'question__text')
    list_filter = ('is_correct', 'session__quiz__title')

    def session_display(self, obj):
        return f"{obj.session.user.username} - {obj.question.text[:50]}"
    session_display.short_description = 'Answer by'

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserQuizSession, UserQuizSessionAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)