from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings as conf_setting
from django.urls import reverse

from quiz_profile.forms import UserRegisterForm, UserPasswordRestForm, UserPasswordRestConfirmForm, UserPasswordChangeForm
from quiz.models import UserCategoryAttempt

def login(request):

    error_message = ''

    if request.user.is_authenticated:
        return redirect('quiz_home')
    
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            django_login(request, user)
            return redirect('quiz_home')
        else:
            error_message = 'Try again! username or password is incorrect'

    context = {
        'title'         :   'Login | Quiz Application',
        'error_message' :   error_message
    }
    return render(request, 'accounts/login.html', context)

def register(request):

    if request.user.is_authenticated:
        return redirect('quiz_home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
            django_login(request, new_user)

            # Send welcome email

            name = form.cleaned_data['first_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            url = reverse('login')
            context = {
                'name' : name,
                'username' : username,
                'email' : email,
                'login_url' : url
            }
            html_template = 'accounts/registration/welcome-email.html'
            html_message = render_to_string(html_template, context, request=request)
            subject = 'Welcome to Quiz Application'
            email_from = conf_setting.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject, html_message, email_from, recipient_list)
            message.send()

            return redirect('quiz_home')
    else:
        form = UserRegisterForm()

    context = {
        'form'  : form,
        'title' : 'Registration | Quiz Application'
    }
    return render(request, 'accounts/register.html', context)

class UserPasswordRest(PasswordResetView):

    form_class = UserPasswordRestForm

    email_template_name = 'accounts/registration/password_reset_email.html'

    subject_template_name = 'accounts/registration/password_reset_subject.txt'

class UserPasswordRestConfirm(PasswordResetConfirmView):

    form_class = UserPasswordRestConfirmForm

class UserPasswordChange(PasswordChangeView):

    form_class = UserPasswordChangeForm
    success_url = 'user_logout'

def callback(request):

    return redirect('quiz_home')

def user_profile(request):

    user = request.user
    user_category = UserCategoryAttempt.objects.filter(user = user)
    total_quiz_attempt = user_category.count()
    highest_score = user_category.order_by('-score').first()
    last_attempt = user_category.order_by('-attempt_time').first()
    achievement = user_category.order_by('-score')[:10]

    context = {
        'total_quiz_attempt' : total_quiz_attempt,
        'highest_score' : highest_score,
        'last_attempt' : last_attempt,
        'achievement' : achievement
    }
    return render(request, 'accounts/profile-page.html', context)

def logout(request):
    
    django_logout(request)
    return redirect('/')

def error_404(request,exception):
    context = {}
    return render(request, 'layout/error_404.html', context)


def error_500(request):
    context = {}
    return render(request, 'layout/error_500.html', context)