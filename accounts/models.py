from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class User(AbstractUser):
    """
    Customized basic Django User model without username,
    but with email field instead.
    """
    username = None
    email = models.EmailField('Adres e-mail', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"
