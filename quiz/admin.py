from django.contrib import admin
from .models import Quiz, Question, Answer

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

class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "book", "owner", "created_at", "updated_at")
    inlines = [QuestionInline]

class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "is_correct", "order", "score", "created_at", "updated_at")
    exclude = ['order']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
