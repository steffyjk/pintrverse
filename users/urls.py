from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import RegistrationView, HomeView, UserProfileUpdateView, UserProfilePageView, OtherUserProfile, \
    FollowUserView, UserFollowingList, UnfollowUserView, ResetPassword, reset_password_confirm, UserFollowerList

app_name = 'users'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('edit-profile/<int:pk>/', UserProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/', UserProfilePageView.as_view(), name='profile'),
    path('other-user-profile/<int:pk>/', OtherUserProfile.as_view(), name='other-user-profile'),
    path('follow-user/<str:user>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow-user/<str:user>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('following-list/', UserFollowingList.as_view(), name='following-list'),
    path('follower-list/', UserFollowerList.as_view(), name='follower-list'),


    path('reset-password/', ResetPassword, name='reset_password'),
    path('reset-password/<uidb64>/<token>/', reset_password_confirm, name='password_reset_confirm'),
]
