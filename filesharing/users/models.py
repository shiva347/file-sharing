from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_ops_user = models.BooleanField(default=False, verbose_name='Operation User')
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
