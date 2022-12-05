from django.urls import path

from quiz import views

urlpatterns = [
    path('quiz-home/', views.quizhome, name = 'quiz_home'),
    path('all-category/', views.all_category, name = 'all_category'),
    path('add-category/', views.add_category, name = 'add_category'),
    path('edit-category/<slug:slug>/', views.edit_category, name = 'edit_category'),
    path('delete-category/<slug:slug>/', views.delete_category, name = 'delete_category'),
    path('all-question/', views.all_question, name = 'all_question'),
    path('add-question/', views.add_question, name = 'add_question'),
    path('edit-question/<slug:slug>/', views.edit_question, name = 'edit_question'),
    path('quiz-category/', views.quiz_category, name = 'quiz_category'),
    path('start-quiz/<slug:category>/', views.start_quiz, name = 'start_quiz'),
    path('submit-answer/<slug:category>/<int:attempt_id>/<int:cat_attempt_id>/', views.submit_answer, name = 'submit_answer'),
    path('quiz-result/<slug:category>/', views.quiz_result, name = 'quiz_result'),
    path('quiz-history/', views.quiz_history, name = 'quiz_history')
]