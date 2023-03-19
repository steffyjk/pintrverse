from django import forms

from pintrverse_app.models import Pin, User


class CreatePinForm(forms.ModelForm):
    class Meta:
        model = Pin
        exclude = ['user']
