from django.db import models
from django.contrib.auth.models import User

import datetime


class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    middle_name = models.CharField('middle_name', max_length=30, null=True)
    birthdate = models.DateField('birthdate', null=True)

    def __str__(self):
        return 'Profile object (%d) of user (%d)' % (self.id, self.user_id.id)


class Profession(models.Model):
    name = models.CharField('name', max_length=50)
    description = models.TextField('description')

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    profession_id = models.ForeignKey(Profession, on_delete=models.CASCADE)
    description = models.TextField('description')

    def __str__(self):
        return '%s %s (%d) - %s' % (self.user_id.first_name,
                                    self.user_id.last_name,
                                    self.user_id.id,
                                    self.profession_id.name)


class Post(models.Model):
    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    title = models.CharField('title', max_length=50)
    content = models.TextField('content')
    create_time = models.DateTimeField('create_time')
    update_time = models.DateTimeField('update_time', null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField('content', max_length=140)
    create_time = models.DateTimeField('create_time')
