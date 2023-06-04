from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)

    # is_customer = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username