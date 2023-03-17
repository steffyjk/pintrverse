from django import forms

from users import constants
from users.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=128)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'mobile_number', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError(constants.PWD_AND_CONFIRM_PWD_ERR)

