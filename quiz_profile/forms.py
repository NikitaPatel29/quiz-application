from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import ValidationError

class UserRegisterForm(UserCreationForm):

    first_name = forms.CharField(widget = forms.TextInput(attrs = {'placeholder' : 'First Name', 'class' : 'form-control'}))
    last_name = forms.CharField(widget = forms.TextInput(attrs = {'placeholder' : 'Last Name', 'class' : 'form-control'}))
    username = forms.CharField(widget = forms.TextInput(attrs = {'placeholder' : 'Username', 'class' : 'form-control'}))
    email = forms.EmailField(widget = forms.TextInput(attrs = {'placeholder' : 'Email', 'class' : 'form-control'}))
    password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder' : 'Password', 'class' : 'form-control'}))
    password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder' : 'Retype password', 'class' : 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class UserPasswordRestForm(PasswordResetForm):

    email = forms.EmailField(widget = forms.TextInput(attrs = {'placeholder' : 'Your Email', 'class' : 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with the specified email address!")
        
        return email

    class Meta:
        model = User
        fields = ['email']

class UserPasswordRestConfirmForm(SetPasswordForm):

    new_password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder' : 'New Password', 'class' : 'form-control'}))
    new_password2 = forms.CharField(label= "Confirm Password", widget = forms.PasswordInput(attrs = {'placeholder' : 'Confirm New password', 'class' : 'form-control'}))

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class UserPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder' : 'Old Password', 'class' : 'form-control'}))
    new_password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder' : 'New Password', 'class' : 'form-control'}))
    new_password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder' : 'Confirm New Password', 'class' : 'form-control'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        