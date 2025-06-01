from django.contrib import admin
from .models import Quiz, Question, Answer, QuestionType

class AnswerInline(admin.TabularInline):
    exclude = ['order']
    model = Answer
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    exclude = ['order']
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "text", "order", "created_at", "updated_at")
    exclude = ['order']
    inlines = [AnswerInline]

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)

        # Auto-create True/False answers
        if is_new and obj.question_type == QuestionType.TRUE_FALSE:
            Answer.objects.bulk_create([
                Answer(question=obj, text="True", is_correct=False, order=1),
                Answer(question=obj, text="False", is_correct=False, order=2),
            ])

class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "book", "owner", "created_at", "updated_at")
    inlines = [QuestionInline]

class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "is_correct", "order", "score", "created_at", "updated_at")
    exclude = ['order']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
