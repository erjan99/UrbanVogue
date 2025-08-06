from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MyUser
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .services import *
from django.conf import settings
from .forms import EditProfileForm, RegisterForm, LoginForm

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
        user_email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=user_email, password=password)
        if user is not None:
            if user.is_2fa_enabled:
                otp = generate_OTP_code()
                user.otp = otp
                user.save()

                send_mail(
                    subject='Code',
                    message=f'Your OTP code is {otp}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=False,
                )

                messages.success(request, 'OTP sent successfully')
                return redirect( 'otp_verification', user.id)
            else:
                login(request, user)
                messages.success(request, 'Welcome back!')
                return redirect('index_view')

        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user':user})

@login_required(login_url='login')
def is_2fa_enabled(request):
    if request.method == 'POST':
        print(request.POST)
        user = request.user

        user.is_2fa_enabled = 'choice' in request.POST
        user.save()
        return redirect('profile_view')


def verify_otp(request, user_id):
    user = MyUser.objects.get(id=user_id)
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        user.save()
        if verify_OTP_code(user_otp, user.otp):
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('index_view')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'otp_verification.html', {'user':user})

def resend_otp(request, user_id):
    user = MyUser.objects.get(id=user_id)
    otp = generate_OTP_code()
    user.otp = otp
    user.save()

    send_mail(
        subject='Code',
        message=f'Your OTP code is {otp}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    messages.success(request, 'OTP resent successfully')
    return redirect('otp_verification', user.id)

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_view')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})
