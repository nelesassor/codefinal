# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from studdybuddy.models import CustomUser, Skill


class UserNameForm(forms.Form):
    username = forms.CharField(max_length=50, label='')

    def clean_username(self):
        username = self.cleaned_data['username']

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("")
        return username


class EmailForm(forms.Form):
    email = forms.EmailField(label='')

    def clean_email(self):
        email = self.cleaned_data['email']

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("")
        return email


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class SimpleForm(forms.Form):
    options = []
    for skill in Skill.objects.all():
        options.append((skill, skill))

    favorite_skills = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'summernote', 'name': 'subject'}
        ),
        choices=options
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
