from .models import Task
from .forms import *

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages


def index(request):
    tasks = Task.objects.all()
    params = {
        'tasks': tasks,
    }
    return render(request, 'tasks/index.html', params)


def create(request):
    if (request.method == 'POST'):
        title = request.POST['title']
        content = request.POST['content']
        task = Task(title=title, content=content)
        task.save()
        return redirect('tasks:index')
    else:
        params = {
            'form': TaskCreationForm(),
        }
        return render(request, 'tasks/create.html', params)


def detail(request, task_id):
    task = Task.objects.get(id=task_id)
    params = {
        'task': task,
    }
    return render(request, 'tasks/detail.html', params)


def edit(request, task_id):
    task = Task.objects.get(id=task_id)
    if (request.method == 'POST'):
        task.title = request.POST['title']
        task.content = request.POST['content']
        task.save()
        return redirect('tasks:detail', task_id)
    else:
        form = TaskCreationForm(initial={
            'title': task.title,
            'content': task.content,
        })
        params = {
            'task': task,
            'form': form,
        }
        return render(request, 'tasks/edit.html', params)


def delete(request, task_id):
    task = Task.objects.get(id=task_id)
    if (request.method == 'POST'):
        task.delete()
        return redirect('tasks:index')
    else:
        params = {
            'task': task,
        }
        return render(request, 'tasks/delete.html', params)

"""Member related functions"""
def member_registration(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            age = form.cleaned_data['age']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return render(request, 'users/registration.html', {'form': form})

            User = get_user_model()
            User.objects.create_user(
                username=username,
                email=email,
                age=age,
                password=password
            )

            messages.success(request, 'Registration successful. Please log in.')
            return redirect('tasks:login')

    else:
        form = MemberCreationForm()

    return render(request, 'users/registration.html', {'form': form})


def member_login(request):
    if request.method == 'POST':
        form = MemberLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('tasks:index')
            else:
                messages.error(request, 'Invalid email or password')

    else:
        form = MemberLoginForm()

    return render(request, 'users/login.html', {'form': form})
