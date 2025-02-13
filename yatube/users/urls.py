# Импортируем из приложения django.contrib.auth нужный view-класс
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordChangeView)

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('logout/', LogoutView.as_view(
        template_name='users/logged_out.html'),
        name='logout'),

    path('signup/', views.SignUp.as_view(), name='signup'),

    path('login/', LoginView.as_view(
        template_name='users/login.html'),
        name='login'),

    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html'),
        name='password_reset_form'),

    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
        name='reset_done'),

    path('password_change_form/', PasswordChangeView.as_view(
        template_name='users/password_change_form.html'),
        name='password_change_form'), ]
