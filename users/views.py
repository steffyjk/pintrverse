from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import CreateView, TemplateView, UpdateView

from pintrverse_app.models import SavedPin, Pin
from users.forms import UserRegistrationForm
from users.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import CustomPasswordResetForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import CustomSetPasswordForm
from django.contrib.auth import get_user_model, login


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
        return redirect(reverse_lazy('home'))


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
        return redirect(reverse_lazy('home'))


User = get_user_model()


def ResetPassword(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user:
                # Generate a token for the user
                token_generator = default_token_generator
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)

                # Build the password reset URL and send it to the user's email
                reset_url = request.build_absolute_uri(f"/users/reset-password/{uid}/{token}/")
                send_mail(
                    'Password Reset',
                    f'Here is the link to reset your password: {reset_url}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
                return render(request, 'users/reset_password_done.html')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'users/reset_password.html', {'form': form})


def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                login(request, user)
                return redirect('home')
        else:
            form = CustomSetPasswordForm(user=user)
        return render(request, 'users/reset_password_confirm.html', {'form': form})
    else:
        return render(request, 'users/reset_password_invalid.html')
