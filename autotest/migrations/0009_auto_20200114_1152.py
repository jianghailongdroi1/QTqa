# Generated by Django 2.0 on 2020-01-14 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autotest', '0008_auto_20200114_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suite',
            name='cronjob',
            field=models.ManyToManyField(db_constraint=False, to='autotest.CronJob'),
        ),
    ]
