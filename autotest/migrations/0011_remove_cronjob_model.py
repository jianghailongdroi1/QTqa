# Generated by Django 2.0 on 2020-01-14 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autotest', '0010_auto_20200114_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cronjob',
            name='model',
        ),
    ]
