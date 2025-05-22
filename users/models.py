from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserManager
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom user model that extends the AbstractUser model.
    """
    username = None
    email = models.EmailField(_("email address"), unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects=UserManager()

    def __str__(self):
        return self.email
