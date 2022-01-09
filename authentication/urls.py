from django.urls import path, include

from authentication.views import PhoneView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('phone/', PhoneView.as_view(), name="auth-login"),
    path('phone-verify/',  VerificationViewSet, name="phone-verify"),
]
