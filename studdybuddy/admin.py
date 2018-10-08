# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from studdybuddy.forms import CustomUserCreationForm, CustomUserChangeForm
from studdybuddy.models import Skill, CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'post_id', 'machted', 'matchedUserID', 'slack_handle', 'phone_number', 'get_own_skills', 'get_want_skills']

    def get_own_skills(self, user):
        return ", ".join([skill.name for skill in user.iHave.all()])

    def get_want_skills(self, user):
        return ", ".join([skill.name for skill in user.iWant.all()])


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Skill)
