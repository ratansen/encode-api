from django.urls import path,include
from .views import LoginView, RegisterUsersView, UserProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name="auth-login"),
    path('register/', RegisterUsersView.as_view(), name="auth-register"),
    path('profile/', UserProfileView.as_view(), name="auth-profile"),
    path('password_reset',
         include('django_rest_passwordreset.urls', namespace='password_reset')),
]
