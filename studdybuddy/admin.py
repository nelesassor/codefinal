# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from studdybuddy.forms import CustomUserCreationForm, CustomUserChangeForm
from studdybuddy.models import Skill, CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'post_id', 'machted', 'matchedUserID']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Skill)
