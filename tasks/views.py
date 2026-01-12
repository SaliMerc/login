from .models import Task
from .forms import *

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout, update_session_auth_hash
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

def member_info(request):
    return render(request, 'users/member-info.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('tasks:index')

def delete_member_page(request):
    return render(request, 'users/cancel-member.html')

def delete_member(request):
    try:
        user = request.user
        user.delete()         

        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('tasks:index')

    except Exception:
        messages.error(request, 'An error occurred while deleting your account.')
        return redirect('tasks:member_info')


def profile_update(request):
    if request.method == 'POST':
        form = MemberUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('tasks:member_info') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MemberUpdateForm(instance=request.user)

    return render(request, 'users/member-edit.html', {'form': form})

def password_change(request):
    if request.method == 'POST':
        form = MemberPasswordChangeForm(request.POST)

        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']

            user = request.user
            if not user.check_password(old_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password != confirm_new_password:
                messages.error(request, 'New passwords do not match.')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user) 
                messages.success(request, 'Password changed successfully.')
                return redirect('tasks:member_info')  

    else:
        form = MemberPasswordChangeForm()

    return render(request, 'users/password-change.html', {'form': form})