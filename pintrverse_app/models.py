from django.db import models

from users.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250, null=False, unique=True)

    def __str__(self):
        return self.name


class Pin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pic = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    about = models.CharField(max_length=250)
    alt_text = models.CharField(max_length=250, null=True)
    destination_link = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name


class SavedPin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'pin')

    def __str__(self):
        return self.pin


class Comment(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_data = models.CharField(max_length=150, null=False)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.comment_data

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)


class Like(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
