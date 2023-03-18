from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import RegistrationView, HomeView, UserProfileUpdateView, UserProfilePageView

app_name = 'users'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/users/home/'), name='logout'),
    path('edit-profile/<int:pk>/', UserProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/', UserProfilePageView.as_view(), name='profile'),
]
