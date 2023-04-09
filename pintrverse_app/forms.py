from django import forms

from pintrverse_app.models import Pin, User,Category,Tag


class CreatePinForm(forms.ModelForm):
    alt_text = forms.CharField(label='Alternate Text', max_length=255)
    class Meta:
        model = Pin
        exclude = ['user']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)