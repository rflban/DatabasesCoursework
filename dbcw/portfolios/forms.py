from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, \
                         TextInput, PasswordInput, \
                         EmailInput, DateInput, \
                         Form, ChoiceField, Textarea

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


class SearchForm(Form):
    searching = CharField()

    searching.label = ''
    searching.widget.attrs.update({
        "type": "text",
        "class": "form-control",
        # "placeholder": "&#xf002",
        # "placeholder": "",
        "placeholder": "\uF002",
        "style": "font-family:Arial, FontAwesome",
        "required": "",
    })


class PortfolioForm(Form):
    values = models.Profession.objects.all()
    choices = []
    for i in range(len(values)):
        choices.append((values[i].name, values[i].name))

    profession = ChoiceField(choices=choices)
    description = CharField(widget=Textarea)

    profession.widget.attrs.update({
        "id": "inputProfession",
        "class": "form-control mb-2",
        "required": "",
    })
    description.widget.attrs.update({
        "id": "inputDescription",
        "class": "form-control",
        "required": "",
        "rows": "10",
    })


class PostForm(Form):
    title = CharField(max_length=50)
    content = CharField(widget=Textarea)

    title.widget.attrs.update({
        "class": "form-control mt-3 mb-3",
        "type": "text",
        "placeholder": "Заголовок",
        "required": "",
    })
    content.widget.attrs.update({
        "id": "autoresizing",
        "class": "form-control",
        "placeholder": "Расскажите о своих достижениях...",
        "rows": "5",
        "required": "",
    })


class CommentForm(Form):
    content = CharField(widget=Textarea, max_length=140)
    content.widget.attrs.update({
        "id": "autoresizing",
        "class": "form-control",
        "placeholder": "Напишите, что думаете по этому поводу...",
        "rows": "2",
        "required": "",
    })
