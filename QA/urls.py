"""QA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from autotest import views
from autotest.myFunctions import reset_overdue_subtask
from autotest import myFunctions
from apscheduler.scheduler import Scheduler
from autotest.myFunctions import scheduler_task_in_startupItems
from django.conf import settings

#添加启动项
sched = Scheduler()  # 实例化，固定格式
@sched.interval_schedule(seconds=settings.SCHEDULED_TASKS_RUN_SETTINGS['interval_time'])  # 装饰器，并设置执行间隔时间，以秒为单位
def mytask():
    scheduler_task_in_startupItems()
sched.start()  # 启动该脚本


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^job_result_add_page/$', views.get_job_result_add_page, name='job_result_add_page'),

    url(r'^job_result_add/$', views.job_result_add, name='job_result_add'),
    url(r'^query_job_result/$', views.job_result_select, name='query_job_result'),
    #对外提供的执行冒烟测试的接口
    url(r'^execute_job_immediately/(?P<project>.*)$', views.excute_job_immediately, name='execute_job_immediately'),
    #调试用新建定时任务的接口
    url(r'^create_cron_job/$', views.create_cron_job, name='create_cron_job'),

    #启动新建的定时任务，创建对应的子任务
    url(r'^start_cronjob_view/(?P<job_id>.*)/$', views.start_cronjob_view, name='start_cronjob_view'),

    #试运行定时任务的接口，入参为定时任务的id
    url(r'^test_run_cronjob/(?P<cronjob_id>.*)$', views.test_run_cronjob),

]
