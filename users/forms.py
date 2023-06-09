from django import forms

from users import constants
from users.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm

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

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=commit)
        user.set_password(user.password)
        user.save()
        return user

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # customize the form fields here, if needed


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # customize the form fields here, if needed

