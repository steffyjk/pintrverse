from django.contrib import admin

from pintrverse_app.models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    pass
