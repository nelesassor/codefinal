import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from . import Skill


class CustomUser(AbstractUser):
    post_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True
    )

    iHave = models.ManyToManyField(
        Skill,
        related_name="iHave",
        help_text='Select a Person for this Skill'
    )

    iWant = models.ManyToManyField(
        Skill,
        related_name="iWant",
        help_text='Select a Person for this Skill'
    )

    machted = models.BooleanField(default=False)
    matchedUserID = models.CharField(max_length=200)

    def __str__(self):
        return self.username
