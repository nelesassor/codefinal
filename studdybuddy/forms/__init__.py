# users/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from studdybuddy.models import CustomUser

from .registration import *


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
