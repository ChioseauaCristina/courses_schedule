from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class CourseFormDefault(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ['user']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=60)
    password = forms.CharField(max_length=60, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1')
