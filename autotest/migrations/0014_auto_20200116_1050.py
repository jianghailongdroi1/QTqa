# Generated by Django 2.0 on 2020-01-16 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autotest', '0013_auto_20200115_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronjob',
            name='status',
            field=models.CharField(choices=[('1', '未执行'), ('2', '执行中'), ('3', '执行异常'), ('4', '执行完成'), ('5', '过期任务')], default='1', max_length=255, verbose_name='执行结果'),
        ),
    ]
