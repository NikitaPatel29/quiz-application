from django.contrib import admin

from quiz.models import QuizCategory, QuizQuestion

admin.site.register(QuizCategory)

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'slug']

admin.site.register(QuizQuestion, QuizQuestionAdmin)
