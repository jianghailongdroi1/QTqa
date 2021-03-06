# Generated by Django 2.0 on 2020-01-15 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autotest', '0011_remove_cronjob_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronjob',
            name='effective_flag',
            field=models.CharField(choices=[('1', '有效'), ('0', '无效')], default='1', max_length=255, verbose_name='是否有效'),
        ),
        migrations.AlterField(
            model_name='cronjob',
            name='enable',
            field=models.CharField(choices=[('0', '未启用'), ('1', '启用')], default='0', max_length=255, verbose_name='是否启用'),
        ),
        migrations.AlterField(
            model_name='cronjob',
            name='iterval_time',
            field=models.IntegerField(default=60, max_length=10, verbose_name='间隔时间(单位:分钟)'),
        ),
        migrations.AlterField(
            model_name='cronjob',
            name='status',
            field=models.CharField(choices=[('1', '未执行'), ('2', '执行中'), ('3', '执行异常'), ('4', '执行完成')], default='1', max_length=255, verbose_name='执行结果'),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='status',
            field=models.CharField(choices=[('1', '未执行'), ('2', '执行中'), ('3', '执行异常'), ('4', '执行完成'), ('5', '过期任务')], max_length=255, verbose_name='执行结果'),
        ),
        migrations.AlterField(
            model_name='suite',
            name='cronjob',
            field=models.ManyToManyField(blank=True, db_constraint=False, to='autotest.CronJob'),
        ),
    ]
