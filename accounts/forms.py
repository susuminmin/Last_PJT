from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(
        label='Username',
        max_length=254,
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):

    username = forms.CharField(
        label='Username',
        max_length=254,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', ]