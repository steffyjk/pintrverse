from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView

from users import forms
from users.forms import UserRegistrationForm
from users.models import User


# Create your views here.
class RegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy("home")


class HomeView(TemplateView):
    template_name = 'home.html'

class LoginPageView(LoginView):
    pass