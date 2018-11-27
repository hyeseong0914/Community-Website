from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from django.contrib.auth.models import User
from django.db.models.query_utils import DeferredAttribute


class RegisterationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='이름을 적어주세요', label='이름')
    email = forms.EmailField(max_length=254, required=True, help_text='이메일을 적어주세요', label='이메일')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')
        help_texts = {
            'username': '30자 이하 문자, 숫자 그리고 @/./+/-/_만 가능합니다.',
        }
        labels = {
            'username': '아이디'
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True, label='아이디')
    password = forms.CharField(label='비밀번호', required=True, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='로그인 유지', required=False, widget=forms.CheckboxInput())

class ProfileChangeForm(UserChangeForm):
    username = forms.CharField(max_length=254, required=True, label='아이디')
    email = forms.EmailField(max_length=254, required=True, label='이메일')
    first_name = forms.CharField(max_length=30, required=True, label='이름')
    class Meta:
        model = User
        fields = {'username', 'first_name', 'email', 'password'}
        labels = {
            'username': '아이디'
        }
        help_texts = {
            'password': '30자 이하 문자, 숫자 그리고 @/./+/-/_만 가능합니다.',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        kwargs.update(initial={
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
        })

        super(ProfileChangeForm, self).__init__(*args, **kwargs)