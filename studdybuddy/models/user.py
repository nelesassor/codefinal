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

    slack_handle = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    study_path = models.CharField(
        max_length=50,
        choices=[
            ("SE", "Software Engineering"),
            ("ID", "Interaction Design"),
            ("PM", "Product Management")
        ],
        default="SE"
    )

    def __str__(self):
        return self.username
