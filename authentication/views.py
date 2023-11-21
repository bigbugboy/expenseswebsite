import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError

from .forms import UserRegisterForm

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': '用户名必须是英文字母和数字'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': '用户名已存在'}, status=409)
        return JsonResponse({'username_valid': True})
    

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError as e:
            return JsonResponse({'email_error': str(e)}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': '邮箱已占用'}, status=409)
        return JsonResponse({'email_valid': True})


class PasswordValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password']
        pwd_lens = len( str(password).strip())
        if pwd_lens < 6:
            return JsonResponse({'password_error': '密码不能少于6位'}, status=400)
        return JsonResponse({'password_valid': True})


class RegisterView(View):

    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        data = request.POST
        username = data['username']
        email = data['email']
        password = data['password']
        # TODO: validate
        form_obj = UserRegisterForm(request.POST)
        if form_obj.is_valid():
            user = User.objects.create_user(username, email, password)
            messages.success(request, '账号注册成功')
            return render(request, 'authentication/register.html')
        
        # error, form_obj.errors is a dict
        for error in form_obj.errors.values():
            messages.error(request, error[0])
        return render(request, 'authentication/register.html', data)

        


