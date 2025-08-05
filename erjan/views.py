from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, logout, authenticate
from .forms import ProfileUpdateForm

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            messages.success(request, 'Account created successfully')
            login(request, user)
            return redirect('index_view')
        messages.error(request, 'Registration Unsuccessful. Invalid information. Please try again.')
    else:
        form = RegisterForm()


    return render(request, 'register.html', context={'form':form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('index_view')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('index_view')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'profile.html', {'form': form})


