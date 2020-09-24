from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, \
                         TextInput, PasswordInput, \
                         EmailInput, DateInput, \
                         Form

from . import models


class UserForm(ModelForm):
    class Meta:
        model = User

        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        ]

        widgets = {
                "username": TextInput(attrs={
                    "class": "form-control",
                    "id": "username",
                    "placeholder": "Имя пользователя",
                    "required": "",
                }),
                "first_name": TextInput(attrs={
                    "class": "form-control",
                    "id": "firstName",
                    "placeholder": "",
                    "required": "",
                    "value": "",
                }),
                "last_name": TextInput(attrs={
                    "class": "form-control",
                    "id": "lastName",
                    "placeholder": "",
                    "required": "",
                    "value": "",
                }),
                "password": PasswordInput(attrs={
                    "class": "form-control",
                    "id": "password",
                    "placeholder": "Пароль",
                    "required": "",
                }),
                "email": EmailInput(attrs={
                    "class": "form-control",
                    "id": "email",
                    "placeholder": "you@example.com",
                }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False


class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile

        fields = [
            'middle_name',
            'birthdate',
        ]

        widgets = {
                "middle_name": TextInput(attrs={
                    "class": "form-control",
                    "id": "middleName",
                    "placeholder": "",
                    "value": "",
                }),
                "birthdate": DateInput(attrs={
                    "type": "date",
                    "class": "form-control",
                    "id": "birthdate",
                })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['middle_name'].required = False
        self.fields['birthdate'].required = False


class AuthUserForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)

    username.widget.attrs.update({
        "type": "username",
        "id": "inputUsername",
        "class": "form-control",
        "placeholder": "Имя пользователя",
        "required": "",
        "autofocus": "",
    })

    password.widget.attrs.update({
        "type": "password",
        "id": "password",
        "class": "form-control mt-2",
        "placeholder": "Пароль",
        "required": "",
    })
