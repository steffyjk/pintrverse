from django.contrib import admin

from pintrverse_app.models import Category, Tag


# Register your models here.
@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass
@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    pass
