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
from autotest import views_job
from autotest import views_project
from autotest import views_suite
from autotest import views_job_result
from autotest import views_jiajia
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
    path('add_project/', views_project.add_project),
    #项目编辑接口
    path('edit_project/', views_project.edit_project),
    # 项目删除接口
    path('delete_project/', views_project.delete_project),
    #项目查询接口(jiajia)
    url(r'^SearchForProject/$', views_project.SearchForProject),
    url(r'^add_suite/SearchForProject/$', views_project.SearchForProject),
    url(r'^project_list/SearchForProject/$', views_project.SearchForProject),
    url(r'^add_task/SearchForProject/$', views_project.SearchForProject),
    url(r'^add_task/SearchForSuites/$', views_suite.SearchForSuite),
    path('project_list/', views_jiajia.project_list),
    path('suite_list/', views_jiajia.suite_list),
    path('suite_list/SearchForSuite/', views_suite.SearchForSuite),


    path('task_list/', views_jiajia.task_list),
    path('reports/', views_jiajia.reports),
    # 新建任务的接口
    url(r'^add_task/$', views_job.create_job),
    # 编辑任务的接口
    url(r'^edit_job/$', views_job.edit_job),
    # 删除任务的接口
    url(r'^delete_job/$', views_job.delete_job),
    # 查询任务的接口
    url(r'^query_jobs/$', views_job.query_jobs),

    # 启动任务，创建对应的子任务
    url(r'^enable_job/$', views_job.enable_job),
    # 暂停任务
    url(r'^unenable_job/$', views_job.unenable_job),

    # 新建suite的接口
    url(r'^add_suite/$', views_suite.add_suite),
    # 删除suite的接口
    url(r'^delete_suite/$', views_suite.delete_suite),
    # 编辑suite的接口
    url(r'^edit_suite/$', views_suite.edit_suite),
    #查询suite接口_post
    url(r'^SearchForSuite/$', views_suite.SearchForSuite),
    # 查询suite接口
    url(r'^SearchForSuite_by_project_id/$', views_suite.SearchForSuite),

    # 查询执行结果接口
    url(r'^query_job_results/$', views_job_result.query_job_results),
]
