from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
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


class OtherUserProfile(generic.TemplateView):
    template_name = 'users/other_user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(OtherUserProfile, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(id=kwargs['pk'])
        if self.request.user.is_authenticated:
            login_user = self.request.user
            other_user = User.objects.get(id=kwargs['pk'])
            if other_user in login_user.following.all():
                context['follow'] = 'yes'
                pins = Pin.objects.filter(user_id=other_user.id).all()
                context['data'] = pins
            else:
                context['follow'] = 'no'

        return context


class FollowUserView(View):
    success_message = "Successfully followed"

    def get(self, request, user):
        user1 = User.objects.filter(id=request.user.id).first()
        user2 = User.objects.filter(username=user).first()
        user1.following.add(user2.id)
        return redirect(to='home')


class UserFollowingList(generic.ListView):
    model = User
    template_name = 'users/user_following_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = user.following.all()
        return queryset


class UnfollowUserView(View):
    success_message = "Successfully Unfollowed"

    def get(self, request, user):
        user1 = User.objects.filter(id=request.user.id).first()
        user2 = User.objects.filter(username=user).first()
        user1.following.remove(user2.id)
        return redirect(to='home')
