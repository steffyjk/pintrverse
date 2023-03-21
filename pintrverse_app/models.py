from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from pintrverse_app.constants import PIN_FILE

User = get_user_model()


# Create your models here.

class CommonField(models.Model):
    created_at = models.DateTimeField(verbose_name=_('Created On'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated On'), auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=250, null=False, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, default=None, unique=True, null=False, blank=False)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Pin(CommonField):
    user = models.ForeignKey(verbose_name=_('User'), to=User, on_delete=models.CASCADE, related_name='pins')
    pin_file = models.FileField(verbose_name=_('Pin File'), upload_to=PIN_FILE)
    title = models.CharField(verbose_name=_('Title'), max_length=150)
    about = models.CharField(verbose_name=_('About'), max_length=250)
    alt_text = models.TextField(verbose_name=_('Alter Text'), blank=True, null=True)
    destination_link = models.URLField(verbose_name=_('Download from URL'), max_length=1000, null=True, blank=True)
    category = models.ForeignKey(verbose_name=_('Category'), to=Category, null=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(to=Tag, related_name='tags', verbose_name=_('Tag'))

    class Meta:
        verbose_name = 'Pin'
        verbose_name_plural = 'Pins'

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.pin_likes.count()

    @property
    def comments_count(self):
        return self.pin_comments.count()


class Board(CommonField):
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    user = models.ForeignKey(verbose_name=_('User'), to=User, on_delete=models.CASCADE, related_name='user_boards')
    pin = models.ForeignKey(verbose_name=_('Pin'), to=Pin, on_delete=models.CASCADE, related_name='pin_boards')

    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'
        unique_together = ('name', 'user', 'pin')

    def __str__(self):
        return self.name


class SavedPin(CommonField):
    user = models.ForeignKey(verbose_name=_('User'), to=User, on_delete=models.CASCADE, related_name='user_saved')
    pin = models.ForeignKey(verbose_name=_('Pin'), to=Pin, on_delete=models.CASCADE, related_name='pin_saved')

    class Meta:
        verbose_name = 'Saved Pin'
        verbose_name_plural = 'Saved Pins'
        unique_together = ('user', 'pin')

    def __str__(self):
        return self.pin.title


class Comment(CommonField):
    pin = models.ForeignKey(verbose_name=_('Pin'), to=Pin, on_delete=models.CASCADE, related_name='pin_comments')
    user = models.ForeignKey(verbose_name=_('User'), to=User, on_delete=models.CASCADE, related_name='user_comments')
    comment = models.CharField(verbose_name=_('Comment'), max_length=250)
    parent = models.ForeignKey(
        verbose_name=_('Parent Comment'),
        to="self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.comment

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)


class Like(models.Model):
    pin = models.ForeignKey(verbose_name=_('Pin'), to=Pin, on_delete=models.CASCADE, related_name='pin_likes')
    user = models.ForeignKey(verbose_name=_('User'), to=User, on_delete=models.CASCADE, related_name='user_likes')
    liked_at = models.DateTimeField(verbose_name=_('Liked At'), auto_now_add=True)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ('user', 'pin')

    def __str__(self):
        return str(self.id)
