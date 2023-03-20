from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, TemplateView, UpdateView

from pintrverse_app.models import SavedPin
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


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'users/profile_edit.html'

    success_url = reverse_lazy('home')

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully')
        return super().form_valid(form)


class UserProfilePageView(generic.TemplateView):
    template_name = 'users/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfilePageView, self).get_context_data(**kwargs)
        context['saved_obj'] = SavedPin.objects.filter(user=self.request.user)
        return context
