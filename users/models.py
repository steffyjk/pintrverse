from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import PROFILE_PICTURE


# Create your models here.
class User(AbstractUser):
    """User model inherited from AbstractUser django's model"""

    mobile_number = models.IntegerField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=PROFILE_PICTURE)

    def __str__(self):
        return self.email

    def __repr__(self):
        return f"This is user {self.username}"
