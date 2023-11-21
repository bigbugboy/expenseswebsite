from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logut', views.LougutView.as_view(), name='logut'),
    path('validate-username', csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    path('validate-pwd', csrf_exempt(views.PasswordValidationView.as_view()), name='validate-pwd'),
]