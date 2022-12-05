from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeView

from quiz_profile import views
from quiz_profile.views import UserPasswordRest, UserPasswordRestConfirm, UserPasswordChange

urlpatterns = [
    path('', views.login, name = 'login'),
    path('user-register/', views.register, name = 'user-register'),
    path('user_logout/', views.logout, name = 'user_logout'),
    path('callback/', views.callback, name = 'callback'),
    path('user-profile/', views.user_profile, name = 'user_profile'),

    #PASSWORD RESET URLS
    path('password-reset/', UserPasswordRest.as_view(template_name = 'accounts/forgot_password.html'), name="password_reset"),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name = 'accounts/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', UserPasswordRestConfirm.as_view(template_name = 'accounts/password_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name = 'accounts/password_reset_complete.html'), name="password_reset_complete"),
    path('change-password', UserPasswordChange.as_view(template_name = 'accounts/password_change.html'), name = 'password_change')
]