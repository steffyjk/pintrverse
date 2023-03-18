# Generated by Django 4.1.7 on 2023-03-18 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated On')),
                ('pin_file', models.FileField(upload_to='pin_files', verbose_name='Pin File')),
                ('title', models.CharField(max_length=150, verbose_name='Title')),
                ('about', models.CharField(max_length=250, verbose_name='About')),
                ('alt_text', models.TextField(blank=True, null=True, verbose_name='Alter Text')),
                ('destination_link', models.URLField(blank=True, max_length=1000, null=True, verbose_name='Download from URL')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pintrverse_app.category', verbose_name='Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pins', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Pin',
                'verbose_name_plural': 'Pins',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated On')),
                ('comment', models.CharField(max_length=250, verbose_name='Comment')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='pintrverse_app.comment', verbose_name='Parent Comment')),
                ('pin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pin_comments', to='pintrverse_app.pin', verbose_name='Pin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='SavedPin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated On')),
                ('pin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pin_saved', to='pintrverse_app.pin', verbose_name='Pin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_saved', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Saved Pin',
                'verbose_name_plural': 'Saved Pins',
                'unique_together': {('user', 'pin')},
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_at', models.DateTimeField(auto_now_add=True, verbose_name='Liked At')),
                ('pin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pin_likes', to='pintrverse_app.pin', verbose_name='Pin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_likes', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'Likes',
                'unique_together': {('user', 'pin')},
            },
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated On')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('pin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pin_boards', to='pintrverse_app.pin', verbose_name='Pin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_boards', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Board',
                'verbose_name_plural': 'Boards',
                'unique_together': {('name', 'user', 'pin')},
            },
        ),
    ]
