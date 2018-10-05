import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a Skill (e.g. programming)')

    def __str__(self):
        return self.name
