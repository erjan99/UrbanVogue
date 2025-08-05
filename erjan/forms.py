from django import forms
from django.contrib.auth.forms import UserCreationForm
from.models import MyUser

class RegisterForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'email')


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'avatar', 'is_2fa_enabled']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_2fa_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

