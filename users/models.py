from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.constants import PROFILE_PICTURE


# Create your models here.
class User(AbstractUser):
    """User model inherited from AbstractUser django's model"""
    PHONE_NUMBER_REGEX = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    email = models.EmailField(verbose_name=_('Email Address'), unique=True, null=False)
    is_email_verified = models.BooleanField(verbose_name=_('Is Email Verified'), default=False)
    following = models.ManyToManyField(
        verbose_name=_("Following"), to='self', related_name='followers', symmetrical=False
    )
    mobile_number = models.CharField(verbose_name=_('Mobile Number')
                                     , validators=[PHONE_NUMBER_REGEX],
                                     max_length=17, null=True, blank=True)
    profile_picture = models.ImageField(
        verbose_name=_('Profile Picture'), upload_to=PROFILE_PICTURE, blank=True, null=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"This is user {self.username}"

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def total_follower(self):
        return self.followers.count()

    @property
    def total_following(self):
        return self.following.count()

    @property
    def total_post(self):
        return self.pins.count()
