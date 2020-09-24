from django.db import models
from django.contrib.auth.models import User

import datetime


class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    middle_name = models.CharField('middle_name', max_length=30, null=True)
    birthdate = models.DateField('birthdate', null=True)
