# Generated by Django 3.1.1 on 2020-09-27 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0008_auto_20200927_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='create_time',
            field=models.DateTimeField(verbose_name='create_time'),
        ),
        migrations.AlterField(
            model_name='post',
            name='update_time',
            field=models.DateTimeField(null=True, verbose_name='update_time'),
        ),
    ]
