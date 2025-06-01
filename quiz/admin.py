from django.contrib import admin
from .models import Quiz

class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")

admin.site.register(Quiz, QuizAdmin)