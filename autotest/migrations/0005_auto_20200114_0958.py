# Generated by Django 2.0 on 2020-01-14 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autotest', '0004_auto_20200114_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='CronJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=255, verbose_name='job名称')),
                ('model', models.CharField(choices=[('cron', 'cron模式'), ('date ', 'date 模式')], max_length=20, verbose_name='定时模式')),
                ('expression', models.CharField(max_length=255, verbose_name='定时公式')),
                ('enable', models.CharField(choices=[('0', '未启用'), ('1', '启用')], max_length=255, verbose_name='是否启用')),
                ('last_status', models.CharField(choices=[('1', '未执行'), ('2', '执行中'), ('3', '执行异常'), ('4', '执行完成')], max_length=255, verbose_name='执行结果')),
                ('description', models.CharField(max_length=255, verbose_name='描述/备注')),
                ('effective_flag', models.CharField(choices=[('1', '有效'), ('0', '无效')], max_length=255, verbose_name='是否有效')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('time_updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name_plural': '定时任务',
                'verbose_name': '定时任务',
                'db_table': 'CronJob',
            },
        ),
        migrations.CreateModel(
            name='Job_result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_name', models.CharField(max_length=255, verbose_name='执行结果名称')),
                ('execute_by', models.CharField(choices=[('1', '自动执行'), ('2', '手动执行'), ('3', '外部触发执行')], max_length=255, verbose_name='执行类型')),
                ('executed_result', models.CharField(max_length=255, verbose_name='执行结果综述')),
                ('link_for_result', models.CharField(max_length=255, verbose_name='报告链接')),
                ('time_start_excute', models.DateTimeField(verbose_name='执行开始时间')),
                ('time_end_excute', models.DateTimeField(auto_now_add=True, verbose_name='执行结束时间')),
            ],
            options={
                'verbose_name_plural': '任务执行结果',
                'verbose_name': '任务执行结果',
                'db_table': '执行结果',
            },
        ),
        migrations.CreateModel(
            name='suite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suite_name', models.CharField(max_length=255, unique=True, verbose_name='suite名称')),
                ('description', models.CharField(max_length=255, verbose_name='描述')),
                ('status', models.CharField(choices=[('1', '须在冒烟测试中执行'), ('2', '不需在冒烟测试中执行')], max_length=10, verbose_name='是否执行冒烟测试')),
                ('effective_flag', models.CharField(choices=[('1', '有效'), ('0', '无效')], max_length=10, verbose_name='是否有效')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('time_updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('cronjob', models.ManyToManyField(to='autotest.CronJob')),
            ],
            options={
                'verbose_name_plural': 'suite表',
                'verbose_name': 'suite表',
                'db_table': 'suite',
            },
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(max_length=255, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='project',
            name='effective_flag',
            field=models.CharField(choices=[('1', '有效'), ('0', '无效')], max_length=255, verbose_name='是否有效'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.CharField(max_length=255, verbose_name='项目名称'),
        ),
        migrations.AlterField(
            model_name='project',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='project',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='suite',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autotest.Project', verbose_name='关联项目'),
        ),
        migrations.AddField(
            model_name='job_result',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autotest.Project', verbose_name='关联项目'),
        ),
        migrations.AddField(
            model_name='cronjob',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autotest.Project', verbose_name='关联项目'),
        ),
    ]
