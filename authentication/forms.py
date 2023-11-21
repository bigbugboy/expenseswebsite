from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=6)
    re_password = forms.CharField(min_length=6)
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if not str(username).isalnum():
            self.add_error('username', '用户名只能是英文字母和数字')
        if User.objects.filter(username=username).exists():
            self.add_error('username', '用户名已存在')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            self.add_error('email', '邮箱已注册')
    
    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            self.add_error('re_password', '两次密码输入不一致')

        return self.cleaned_data