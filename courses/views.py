from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


def register(request):
    form = UserCreationForm(request.POST)
    widgets = forms.TextInput(attrs={'class': "text-field"})
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'courses/register.html', {'form': form})


def login_page(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in!'
                return redirect('/')
            else:
                message = 'Login failed'
    return render(request, 'courses/login.html', context={'form': form, 'message': message})


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):
    courses = Course.objects.filter(user=request.user)
    filtered_courses = None
    search_input = request.GET.get('search-text')

    form = CourseForm()

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user = user.save()
        return redirect('/')

    if request.method == 'GET':
        if search_input:
            filtered_courses = courses.filter(title__contains=search_input)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    context = {'courses': courses, 'form': form, 'days': days, 'filtered_courses': filtered_courses,
               'search_input': search_input}
    return render(request, 'courses/courses.html', context)


@login_required
def update_course(request, pk):
    course = Course.objects.get(id=pk)

    form = CourseFormDefault(instance=course)
    if request.method == 'POST':
        form = CourseFormDefault(request.POST, instance=course)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'form': form}

    return render(request, 'courses/update_course.html', context)


@login_required
def delete_course(request, pk):
    course = Course.objects.get(id=pk)

    if request.method == 'POST':
        course.delete()
        return redirect('/')

    context = {'course': course}

    return render(request, 'courses/delete_course.html', context)
