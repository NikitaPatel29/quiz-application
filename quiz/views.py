from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_setting

from datetime import timedelta

from quiz.models import QuizCategory, QuizQuestion, UserCategoryAttempt
from quiz.models import QuizProfileManager, UserCategoryManager
from quiz.forms import QuizCategoryForm, QuizQuestionForm

@login_required
def quizhome(request):

    context = {}
    return render(request, 'quiz/home.html', context)


@login_required
def all_category(request):

    category_data = QuizCategory.objects.all()

    

    context = {
        'category_data' : category_data
    }
    return render(request, 'quiz/all-category.html', context)

@login_required
def add_category(request):

    error_message = ''
    if request.method == 'POST':
        form = QuizCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_category')
        else:
            error_message = 'Something went wrong !!!'
    else:
        form = QuizCategoryForm()

    context = {
        'form' : form,
        'error_message' : error_message
    }
    return render(request, 'quiz/add-category.html', context)

@login_required
def edit_category(request, slug):

    error_message = ''
    quiz_data = QuizCategory.objects.get(slug=slug)
    
    if request.method == 'POST':
        form = QuizCategoryForm(request.POST, request.FILES, instance = quiz_data)
        if form.is_valid():
            form.save()
            return redirect('all_category')
        else:
            error_message = 'Something went wrong !!!'
    else:
        form = QuizCategoryForm(instance = quiz_data)
        
    context = {
        'form' : form,
        'error_message' : error_message,
        'quiz_data' : quiz_data
    }
    return render(request, 'quiz/update-category.html', context)

@login_required
def delete_category(request, slug):

    if request.method == 'POST':
        category = QuizCategory.objects.get(slug=slug)
        category.delete()
    return redirect('all_category')

@login_required
def all_question(request):

    question_data = QuizQuestion.objects.all()
    context = {
        'question_data' : question_data
    }
    return render(request, 'quiz/all-question.html', context)

@login_required
def add_question(request):
    
    error_message = ''
    if request.method == 'POST':
        form = QuizQuestionForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            return redirect('all_question')
        else:
            print(form.errors.as_data())
            error_message = 'Something went wrong !!!'
    else:
        form = QuizQuestionForm()
    
    context = {
        'form' : form,
        'error_message' : error_message
    }
    return render(request, 'quiz/add-question.html', context)

@login_required
def edit_question(request, slug):
    
    error_message = ''
    question_data = QuizQuestion.objects.get(slug=slug)
    if request.method == 'POST':
        form = QuizQuestionForm(request.POST, instance = question_data)
        if form.is_valid():
            form.save()
            return redirect('all_question')
        else:
            error_message = 'Something went wrong !!!'
    else:
        form = QuizQuestionForm(instance = question_data)
        
    context = {
        'form' : form,
        'error_message' : error_message,
        'question_data' : question_data
    }
    return render(request, 'quiz/update-question.html', context)

@login_required
def quiz_category(request):

    category_data = QuizCategory.objects.all()
   
    categorydata = []
    for data in category_data:
        total_question = QuizProfileManager().total_question(data.id)
        if total_question > 0:
            categorydata.append(data)

    context = {
        'category_data' : categorydata
    }
    return render(request, 'quiz/quiz.html', context)

@login_required
def start_quiz(request, category):

    user = request.user
    quiz_category = QuizCategory.objects.get(slug=category)

    UserCategoryManager().get_category_attempt(user, quiz_category)

    category_attempt = UserCategoryManager().fetch_category_attempt(user, quiz_category).first()
    start_time = category_attempt.attempt_time
    end_time = start_time + timedelta(hours = conf_setting.LAST_QUIZ_ATTEMPT)

    quiz_question = QuizProfileManager().get_new_question(user, quiz_category, start_time, end_time)
    if quiz_question is not None:
        attempt_id = QuizProfileManager().create_attempt(user, quiz_category, quiz_question)
    else:
        return redirect(quiz_result, category = category)

    total_question = QuizProfileManager().total_question(quiz_category)
    total_attempts = QuizProfileManager().attempt_question(user, quiz_category, start_time, end_time)

    context = {
        'category' : quiz_category,
        'question' : quiz_question,
        'attempt_id' : attempt_id,
        'total_question' : total_question,
        'total_attempts' : total_attempts,
        'category_attempt_id' : category_attempt.id
    }
    return render(request, 'quiz/play-quiz.html', context)

@login_required
def submit_answer(request, category, attempt_id, cat_attempt_id):

    if request.method == 'POST' and 'submit' in request.POST:

        answer = request.POST['answer']
        QuizProfileManager().update_attempt(attempt_id, answer)
        QuizProfileManager().update_score(attempt_id, answer, cat_attempt_id)

    return redirect('start_quiz', category = category)

@login_required
def quiz_result(request, category):

    user = request.user
    quiz_category = QuizCategory.objects.get(slug=category)

    category_attempt = UserCategoryManager().fetch_category_attempt(user, quiz_category).first()
    total_question = QuizProfileManager().total_question(quiz_category)
    rightans = category_attempt.score

    percentage = (rightans * 100) / total_question

    context = {
        'total_question' : total_question,
        'right_answer' : int(rightans),
        'percentage' : percentage,
        'category' : quiz_category
    }

    return render(request, 'quiz/quiz-result.html', context)

@login_required
def quiz_history(request):

    user = request.user
    quiz_category = []
    category_attempt = []
    category_data = QuizCategory.objects.all()
    if request.method == 'POST':
        category = request.POST['category']
        quiz_category = QuizCategory.objects.get(slug=category)
        category_attempt = UserCategoryAttempt.objects.filter(user = user, category = quiz_category)

    context = {
        'category' : quiz_category,
        'category_attempt' : category_attempt,
        'category_data' : category_data,
        'method' : request.method
    }
    return render(request, 'quiz/quiz-history.html', context)