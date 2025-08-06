from django.urls import path
from .views import *

urlpatterns = [
    # Authentication
    path('register/', user_register, name='register_view'),
    path('logout/', user_logout, name='logout_view'),
    path('login/', user_login, name='login_view'),

    # Profile
    path('profile/', profile_view, name='profile_view'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    # 2FA
    path('change_2fa/', is_2fa_enabled, name='change_2fa'),
    path('otp_verification/<int:user_id>', verify_otp, name='otp_verification'),
    path('resend_otp/<int:user_id>', resend_otp, name='resend_otp')
]