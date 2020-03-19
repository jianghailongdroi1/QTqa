# Generated by Django 2.0 on 2020-01-14 09:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autotest', '0009_auto_20200114_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cronjob',
            name='expression',
        ),
        migrations.AddField(
            model_name='cronjob',
            name='iterval_time',
            field=models.IntegerField(default=60, max_length=10, verbose_name='间隔时间'),
        ),
        migrations.AddField(
            model_name='cronjob',
            name='maximum_times',
            field=models.IntegerField(default=100, max_length=10, verbose_name='最大执行次数'),
        ),
        migrations.AddField(
            model_name='cronjob',
            name='time_start_excute',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='开始执行时间'),
        ),
        migrations.AlterField(
            model_name='cronjob',
            name='model',
            field=models.CharField(choices=[('1', '仅执行一次'), ('2 ', '多次执行')], max_length=20, verbose_name='定时模式'),
        ),
    ]