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

from django.views.generic import RedirectView

#添加启动项
sched = Scheduler()  # 实例化，固定格式
@sched.interval_schedule(seconds=settings.SCHEDULED_TASKS_RUN_SETTINGS['interval_time'])  # 装饰器，并设置执行间隔时间，以秒为单位
def mytask():
    scheduler_task_in_startupItems()
sched.start()  # 启动该脚本


urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^job_result_add_page/$', views.get_job_result_add_page, name='job_result_add_page'),
    #
    # url(r'^job_result_add/$', views.job_result_add, name='job_result_add'),
    # url(r'^query_job_result/$', views.job_result_select, name='query_job_result'),
    #
    # #调试用新建定时任务的接口
    # url(r'^create_cron_job/$', views.create_cron_job, name='create_cron_job'),
    #
    # #启动新建的定时任务，创建对应的子任务
    # url(r'^start_cronjob_view/(?P<job_id>.*)/$', views.start_cronjob_view, name='start_cronjob_view'),
    #
    # #试运行定时任务的接口，入参为定时任务的id
    # url(r'^test_run_cronjob/(?P<cronjob_id>.*)$', views.test_run_cronjob),

    #20200204重构
    # 测试接口
    url(r'^test/', views.test_function),

    # 调试用，执行subtask表中所有子任务
    url(r'^excute_subtasks', views.excute_all_subtasks),

    # 对外提供的执行冒烟测试的接口
    url(r'^excute_job_by_thirdParty/(?P<project_code>.*)$', views.excute_job_by_thirdParty,
        name='excute_job_by_thirdParty'),

    #新建项目
    path('add_project/', views.add_project),
    #项目列表展示
    path('project_list/', views.list),
    #项目查询接口
    url(r'^SearchForProject/$', views.SearchForProject),

    # 新建任务的接口
    url(r'^create_job/$', views.create_job),
    # 编辑任务的接口
    url(r'^edit_job/$', views.edit_job),
    # 删除任务的接口
    url(r'^delete_job/$', views.delete_job),
    #查询job
    url(r'^query_jobs/$', views.query_jobs),
    # 查询job_detail
    url(r'^query_job_detail/$', views.query_job_detail),

    # 启动任务，创建对应的子任务
    url(r'^enable_job/$', views.enable_job),
    # 暂停任务
    url(r'^unenable_job/$', views.unenable_job),

    # 新建suite的接口
    url(r'^create_suite/$', views.add_suite),
    # 编辑suite的接口
    url(r'^delete_suite/$', views.delete_suite),
    # 编辑suite的接口
    url(r'^edit_suite/$', views.edit_suite),
    #查询suite接口
    url(r'^SearchForSuite/$', views.SearchForSuite),

    # 查询执行结果接口
    url(r'^query_job_results/$', views.query_job_results),
]
