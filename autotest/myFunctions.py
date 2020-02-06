# -*- coding:utf-8 -*-
from httprunner.api import HttpRunner
from django.http import HttpResponse,request
import datetime
# from httprunner.report.html.gen_report import gen_html_report
import time
import requests
import json
from django.conf import settings
from autotest import models

#获取当前时间
def get_current_time():
    time_stamp = time.time()  # 当前时间的时间戳
    local_time = time.localtime(time_stamp)  #
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    return str_time

#执行suite
def run_httprunnner_script(suites):
    kwargs=settings.HTTPRUNNER_RUN_SETTINGS
    runner = HttpRunner(**kwargs)
    #获取报告地址
    result_runner = runner.run(suites)
    summary = runner.summary
    #将报告放到summary中去
    summary["reportpath"]=result_runner
    print("summary:"+summary)

    return summary

# #启动一个定时任务
# def start_cronjob(job_id):
#     exsit_flag = models.CronJob.objects.filter(id = job_id,effective_flag=1).count()
#     if exsit_flag == 0:
#         return "当前任务不存在或无效"
#
#     #获取job的信息：模式和 公式
#     job_obj = models.CronJob.objects.filter(id=job_id, effective_flag=1).values('model','expression').first()
#     model = job_obj["model"]
#     expression = job_obj["expression"]
#
#     #根据job信息获取对应的suite
#     suite_objs = models.suite.objects.filter(cronjob__suite__project_id=job_id).values('suite_name').all()
#     suite_list = []
#     for suite_obj in suite_objs:
#         suite_list.append(suite_obj['suite_name'])
#
#     # 根据suite获取project(仅取第一个suite)
#     project_obj = models.Project.objects.filter(suite__suite_name=suite_list[0]).values('project_code').first()
#     project_code = project_obj["project_code"]
#
#     # 根据项目获取项目的testsuites存放在位置
#     project_testsuites_path = get_testsuitesPath_by_projectCode(project_code)
#
#     #将suite名称和项目的testsuites路径进行拼接
#     suite_final_path_list = []
#     for i in suite_list:
#         i = project_testsuites_path + i
#         suite_final_path_list.append(i)
#     print("suite_final_path_list:",suite_final_path_list)
#
#     #设置定时任务
#         #1/检查公式是否正确（暂时不做）
#         #2/设置定时任务
#     scheduler = BlockingScheduler()
#     scheduler.add_job(func=tick,trigger="cron", hour=17, minute=46)
#
#     # scheduler.add_job(func=tick1,args=['  testP  '],trigger="cron", hour=17, minute=46)
#     # scheduler.add_job(func=tick1,args=("  testp1 "),trigger="cron", hour=17, minute=30)
#
#     try:
#         scheduler.start()
#         print('dsafjajsdfjda')
#     except (KeyboardInterrupt, SystemExit):
#         scheduler.shutdown()
#
#     return "测试程序"

def get_testsuitesPath_by_projectCode(project_code):
    #获取执行suite时的环境,在setting中配置
    httprunner_project_path = settings.HTTPRUNNER_PROJECT_PATH[project_code]
    suite_path = httprunner_project_path + '\\testsuites\\'
    return suite_path

def excute_scheduled_tasks():
    #定时任务间隔时间
    interval_time = settings.SCHEDULED_TASKS_RUN_SETTINGS['interval_time']

    #将过期subtask的任务重置为过期
    reset_overdue_subtask()

    #查询 预期之间时间在区间内的subtask
    subtask_objs = search_subtask_to_excuted(interval_time)

    # 执行查询到的subtask
    if subtask_objs is not None:
        excute_subtasks(subtask_objs)

    #查看子任务的状态，然后看是否要更新 定时任务表
    reset_cronjob_status()

def reset_overdue_subtask():
    now = datetime.datetime.now()
    #将 预期的执行时间小于现在的任务重置状态
    models.Subtask.objects.filter(status=1, time_excepte_excuted__lt=now).update(status = 5)

def reset_cronjob_status():
    #获取定时任务表中有哪些执行中的任务
    cronjob_count = models.CronJob.objects.filter(enable=1,status__in=[2,3]).count()
    if cronjob_count == 0:
        return HttpResponse("没有运行中的定时任务")
    else:
        for cronjob_obj in models.CronJob.objects.filter(enable=1,status__in=[2,3]).all():
            # 按照每个定时任务去查看对应的子任务总数，分别有哪些
            #子任务总数
            subtask_objs_count = models.Subtask.objects.filter(cronjob=cronjob_obj,effective_flag=1).count()
            #未执行的总数
            subtask_objs_status1_count = models.Subtask.objects.filter(cronjob=cronjob_obj,effective_flag=1,status=1).count()

            # #执行中的总数
            # subtask_objs_status2_count = models.Subtask.objects.filter(cronjob=cronjob_obj,effective_flag=1,status=2).count()
            # #执行异常的总数
            # subtask_objs_status3_count = models.Subtask.objects.filter(cronjob=cronjob_obj,effective_flag=1,status=3).count()
            # #执行完成的总数
            # subtask_objs_status4_count = models.Subtask.objects.filter(cronjob=cronjob_obj,effective_flag=1,status=4).count()
            #过期的任务总数
            subtask_objs_status5_count = models.Subtask.objects.filter(cronjob=cronjob_obj,effective_flag=1,status=5).count()

            #最近一次子任务的状态
            last_status = models.Subtask.objects.filter(cronjob=cronjob_obj, effective_flag=1).order_by('time_updated').last().status

            #所有子任务都过期时，定时任务状态为 已过期，已启用状态
            if subtask_objs_count == subtask_objs_status5_count:
                # print('所有子任务都过期时，定时任务状态为 已过期，已启用状态')
                models.CronJob.objects.filter(id=cronjob_obj.id).update(status=5)

            #没有未执行的子任务，且最近一次执行的子任务状态为执行成功， 已完成，已启用状态
            elif (subtask_objs_status1_count == 0 and  last_status == '4'):
                # print('没有未执行的子任务，且最近一次执行的子任务状态为执行成功， 已完成，已启用状态')
                models.CronJob.objects.filter(id=cronjob_obj.id).update(status=4)

            #最近一次执行的任务状态为 执行异常，定时任务状态为 异常，已启用状态
            elif  last_status == '3':
                # print('最近一次执行的任务状态为 执行异常，定时任务状态为 异常，已启用状态')
                models.CronJob.objects.filter(id=cronjob_obj.id).update(status=3)
            else:
                print("不更新定时任务状态")

#重构后的查询待执行子任务方法，返回待执行的子任务对象列表
def search_subtask_to_excuted(interval_time):
    now = datetime.datetime.now()
    #下一次轮训任务的开始时间,为配置的时间
    next_scheduler_time = now + datetime.timedelta(seconds= interval_time)
    print("next_scheduler_time:"+str(next_scheduler_time))
    last_scheduler_time = now - datetime.timedelta(seconds= interval_time)
    print("last_scheduler_time:"+str(last_scheduler_time))


    number_subtasks_to_excuted = models.Subtask.objects.filter(status=1, time_excepte_excuted__range=(last_scheduler_time,next_scheduler_time)
                                         ).count()

    print("number_subtasks_to_excuted:",number_subtasks_to_excuted)

    if number_subtasks_to_excuted == 0:
        return None
    else:
        #返回需要执行的定时子任务的列表
        subtask_objs = models.Subtask.objects.filter(status=1, time_excepte_excuted__range=(last_scheduler_time,next_scheduler_time)).all()
        return subtask_objs

#重构后的执行子任务方法
def excute_subtasks_objs(subtask_objs):
    print('            subtask_objs:' + str(subtask_objs))
    for subtask in subtask_objs:
        try:
            #子任务状态更新为 执行中
            subtask.status = '2'
            subtask.save()
            #执行
            excute_single_subtask(subtask)
            # 子任务状态更新为 执行完成
            subtask.status = '4'
            subtask.save()
        except Exception:
            subtask.status = '3'
            subtask.save()

#重构后的执行子任务
def excute_single_subtask(single_subtask):
    cronjob = single_subtask.cronjob
    project_code = cronjob.project.project_code
    excuter = cronjob.type
    print("===========================================")
    print("excuter:"+excuter)
    print("===========================================")


    #根据定时任务获取相关的suites
    suite_dic = cronjob.suite_set.filter(effective_flag=1).values("suite_name")

    # 获取项目的根目录，并拼接
    suite_path = get_project_basedir(project_code) + '\\testsuites\\'
    suite_list = []
    for i in suite_dic:
        suite_list.append(suite_path + i["suite_name"])

    #跑每个suite
    for suite in suite_list:
        print("-----------------------------")
        result = run_httprunnner_script(suite)
        print("-----------------------------")

        report_path = result['reportpath']
        start_time = result['time']['start_datetime']
        summary = result['stat']['testcases']
        result_name =cronjob.job_name + '任务在' + start_time + "执行的结果"
        print( 'result_name:'+result_name)

        # 将执行结果放入表中
        project_obj = cronjob.project
        models.Job_result.objects.create(result_name=result_name, project=project_obj,
                                         cronjob = cronjob,
                                         subtask = single_subtask,
                                          executed_result=summary,
                                         link_for_result=report_path, time_start_excute=start_time)


def test_run_cronjob(cronjob_id):
    cronjob_obj = models.CronJob.objects.filter(id = cronjob_id)[0]

    project_code = cronjob_obj.project.project_code

    #根据定时任务获取相关的suites
    if cronjob_obj.suite_set.filter(effective_flag=1).count() == 0:
        return  HttpResponse('没有关联的suite')
    suite_dic = cronjob_obj.suite_set.filter(effective_flag=1).values("suite_name")

    # 获取项目的根目录，并拼接
    suite_path = get_project_basedir(project_code) + '\\testsuites\\'
    suite_list = []
    for i in suite_dic:
        suite_list.append(suite_path + i["suite_name"])

    try:
        #跑每个suite
        for suite in suite_list:
            result = run_httprunnner_script(suite)
            report_path = result['reportpath']
            start_time = result['time']['start_datetime']
            summary = result['stat']['testcases']
            result_name = cronjob_obj.job_name + '任务在' + start_time + "手动触发执行的结果"

            # 将执行结果放入表中
            project_obj = cronjob_obj.project
            models.Job_result.objects.create(result_name=result_name, project=project_obj,
                                             execute_by=3, executed_result=summary,
                                             link_for_result=report_path, time_start_excute=start_time)

        cronjob_obj.status = '6'
        cronjob_obj.save()

        return HttpResponse(' 试运行成功！')

    except Exception:
        cronjob_obj.status = '3'
        cronjob_obj.save()
        return HttpResponse(' 试运行失败！')


def get_project_basedir(project_code):
    # 获取执行suite时的环境,在setting中配置
    httprunner_project_path = settings.HTTPRUNNER_PROJECT_PATH[project_code]
    print("httprunner_project_path:", httprunner_project_path)
    return httprunner_project_path

#启动项功能
def scheduler_task_in_startupItems():
    print("===================================================")
    print("this is scheduler_task_in_startupItems")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # excute_scheduled_tasks()
    print("===================================================")

#重构第三方调用接口生成任务的方法
# 接口被调用后，查询是否存在主任务，存在则新增其子任务
def create_new_subtask(project_code):
    res={"status":200,"msg":"操作成功"}
    #查询是否存在对应的项目
    project_count = models.Project.objects.filter(effective_flag=1,project_code=project_code).count()
    if project_count != 1:
        res["status"] = 400
        res["msg"]="project code错误"
        # print('查询是否存在对应的项目')
    else:
        # print('查询是否存在对应项目的 用于“第三方调用”的主任务')
        project_obj = models.Project.objects.filter(effective_flag=1).first()
        #查询是否存在对应项目的 用于“第三方调用”的主任务
        cronjob_count = models.CronJob.objects.filter(effective_flag=1,status =2,
                                                      type = 'called_task',
                                                      project = project_obj).count()
        if cronjob_count == 0:
            res["status"] = 400
            res["msg"] = "不存在对应的任务"
        else:
            # print('根据查询到的主任务新增子任务')
            cronjob_obj = models.CronJob.objects.filter(effective_flag=1, status=2, type='called_task',
                                                          project=project_obj).first()
            # 根据查询到的主任务新增子任务
            models.Subtask.objects.create(cronjob=cronjob_obj,
                                          time_excepte_excuted=get_current_time())
            # print(res)
            # print(json.dumps(res))

    return HttpResponse(json.dumps(res))

#重构执行子任务的方法
def excute_subtasks():
    #定时任务间隔时间
    interval_time = settings.SCHEDULED_TASKS_RUN_SETTINGS['interval_time']

    #将过期subtask的任务重置为过期
    # reset_overdue_subtask()

    #查询 预期之间时间在区间内的subtask
    subtask_objs = search_subtask_to_excuted(interval_time)

    # 执行查询到的subtask
    if subtask_objs is not None:
        print('subtask_objs:' + str(subtask_objs))
        excute_subtasks_objs(subtask_objs)

    #查看子任务的状态，然后看是否要更新 定时任务表
    # reset_cronjob_status()
    return HttpResponse("test")
