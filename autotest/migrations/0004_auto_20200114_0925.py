# Generated by Django 2.0 on 2020-01-14 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autotest', '0003_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_code',
            field=models.CharField(max_length=50, unique=True, verbose_name='项目code'),
        ),
    ]