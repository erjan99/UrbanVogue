from django.urls import path
from .views import *

urlpatterns = [
    # Authentication
    path('register/', user_register, name='register_view'),
    path('logout/', user_logout, name='logout_view'),
    path('login/', user_login, name='login_view'),

    # Profile
    path('profile/', profile_view, name='profile_view')
]