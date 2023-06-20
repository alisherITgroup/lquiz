from django.contrib import admin
from .models import Question, Quiz, Option, Rating

@admin.register(Quiz)
class QuizModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'correct']

@admin.register(Option)
class OptionModelAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Rating)
class RatingModelAdmin(admin.ModelAdmin):
    list_display = ['author', 'quiz', 'score']