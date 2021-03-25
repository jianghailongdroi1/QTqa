# Generated by Django 2.0 on 2020-01-15 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autotest', '0012_auto_20200115_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='effective_flag',
            field=models.CharField(choices=[('1', '有效'), ('0', '无效')], default=1, max_length=255, verbose_name='是否有效'),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='status',
            field=models.CharField(choices=[('1', '未执行'), ('2', '执行中'), ('3', '执行异常'), ('4', '执行完成'), ('5', '过期任务')], default=1, max_length=255, verbose_name='执行结果'),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='time_excepte_excuted',
            field=models.DateTimeField(verbose_name='期望执行时间'),
        ),
    ]