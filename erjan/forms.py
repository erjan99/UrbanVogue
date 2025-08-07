from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class RegisterForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'email')


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'about_user', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

