from django.db import models
import datetime


class Project(models.Model):
    '''
    项目信息表
    '''
    project_code = models.CharField(max_length=50,verbose_name="项目code",null=False,unique=True)
    project_name = models.CharField(max_length=255,verbose_name="项目名称",null=False)
    description = models.CharField(max_length=255,verbose_name="描述")

    EFFECTIVE_CHOICES = (
        ('1', '有效'),
        ('0', '无效')
    )
    effective_flag = models.CharField(max_length=255,choices=EFFECTIVE_CHOICES,verbose_name="是否有效",default=1)
    time_created = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    time_updated = models.DateTimeField(verbose_name='更新时间',auto_now=True)

    class Meta:
        db_table = 'project'
        verbose_name = u"项目信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project_name


class CronJob(models.Model):
    '''
    任务表
    '''
    project = models.ForeignKey("Project", on_delete=models.CASCADE,verbose_name='关联项目')
    job_name = models.CharField(max_length=255,verbose_name="job名称",null=False)

    #仅执行一次时，填写 开始执行时间,最大执行次数填 1
    time_start_excute = models.DateTimeField(default=datetime.datetime.now,verbose_name='开始执行时间')

    iterval_time = models.IntegerField(default=0,verbose_name='间隔时间(单位:分钟)')

    #限制生成的子任务的个数。
    maximum_times = models.IntegerField(default=0,verbose_name='执行次数')

    TYPE_CHOICES = (
        ('timing_task', '定时任务'),
        ('instant_task', '立即执行任务'),
        ('called_task', '第三方调用任务')
    )
    type = models.CharField(max_length=255,choices=TYPE_CHOICES,verbose_name="任务类型",null=False,default='timing_task')

    STATUS_CHOICES = (
        ('1', '未执行'),
        ('2', '执行中'),
        ('3', '执行异常'),
        ('4', '执行完成'),
        ('5', '过期任务')
    )
    status = models.CharField(max_length=255,choices=STATUS_CHOICES,verbose_name="执行结果",null=False,default='1')
    description = models.CharField(max_length=255,verbose_name="描述/备注")
    ENABLE_CHOICES = (
        ('0', '未启用'),
        ('1', '已启用'),
        ('2', '已停用'),
    )
    enable = models.CharField(max_length=5,choices=ENABLE_CHOICES,verbose_name="是否启用",null=False,default='0')

    EFFECTIVE_CHOICES = (
        ('1', '有效'),
        ('0', '无效')
    )
    effective_flag = models.CharField(max_length=5,choices=EFFECTIVE_CHOICES,verbose_name="是否有效",null=False,default='1')
    time_created = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    time_updated = models.DateTimeField(verbose_name='更新时间',auto_now=True)

    class Meta:
        db_table = 'CronJob'
        verbose_name = u"定时任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.job_name


class Subtask(models.Model):
    '''
    定时子任务表
    '''
    cronjob = models.ForeignKey("CronJob", on_delete=models.CASCADE,verbose_name='所属定时任务')

    time_excepte_excuted = models.DateTimeField(verbose_name='期望执行时间')

    STATUS_CHOICES = (
        ('1', '未执行'),
        ('2', '执行中'),
        ('3', '执行异常'),
        ('4', '执行完成'),
        ('5', '过期任务')
    )
    status = models.CharField(max_length=5,choices=STATUS_CHOICES,verbose_name="执行结果",default=1)

    EFFECTIVE_CHOICES = (
        ('1', '有效'),
        ('0', '无效')
    )
    effective_flag = models.CharField(max_length=2,choices=EFFECTIVE_CHOICES,verbose_name="是否有效",null=False,default=1)
    time_created = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    time_updated = models.DateTimeField(verbose_name='更新时间',auto_now=True)

    class Meta:
        db_table = 'Subtask'
        verbose_name = u"定时任务的子任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.time_excepte_excuted.strftime("%Y-%m-%d %H:%M:%S")


class Job_result(models.Model):
    '''
    任务执行结果表
    '''
    result_name = models.CharField(max_length=255,verbose_name="执行结果名称",null=False)
    project = models.ForeignKey("Project", on_delete=models.CASCADE,verbose_name='关联项目')
    cronjob = models.ForeignKey("CronJob",on_delete=models.CASCADE,verbose_name="关联任务")
    subtask = models.ForeignKey("Subtask",on_delete=models.CASCADE,verbose_name="关联子任务")

    executed_result = models.CharField(max_length=255,verbose_name="执行结果综述",null=False)
    link_for_result = models.CharField(max_length=255,verbose_name="报告链接",null=False)
    time_start_excute = models.DateTimeField(verbose_name='执行开始时间')
    time_end_excute = models.DateTimeField(verbose_name='执行结束时间',auto_now_add=True)

    class Meta:
        db_table = 'Job_result'
        verbose_name = u"任务执行结果"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.result_name


class suite(models.Model):
    '''
    suite表
    '''
    suite_name = models.CharField(max_length=255,verbose_name="suite名称",null=False,unique=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE,verbose_name='关联项目',null=False)
    cronjob=models.ManyToManyField(to="CronJob",blank=True,db_constraint = False)

    description = models.CharField(max_length=255,verbose_name="描述")

    EFFECTIVE_CHOICES = (
        ('1', '有效'),
        ('0', '无效')
    )
    effective_flag = models.CharField(max_length=10,choices=EFFECTIVE_CHOICES,verbose_name="是否有效",default=1)
    time_created = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    time_updated = models.DateTimeField(verbose_name='更新时间',auto_now=True)

    class Meta:
        db_table = 'suite'
        verbose_name = u"suite表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.suite_name


