from django.contrib import admin
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Profession)
admin.site.register(models.Portfolio)
admin.site.register(models.Post)
admin.site.register(models.Comment)
