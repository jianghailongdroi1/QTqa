import datetime

from django.shortcuts import render
from django.http import HttpResponse,request
from autotest import models
from django.conf import settings
from autotest import myFunctions

# Create your views here.
def get_job_result_add_page(request):
    return render(request,"job_result_add_page.html")

#调试用
def job_result_add(request):
    if request.method == "GET":
        project_obj = models.Project.objects.filter(id=2)[0]
        models.Job_result.objects.create(result_name='执行结果3',project = project_obj,execute_by=1,executed_result='执行结果总数',
                                         link_for_result='weriuweriu',time_start_excute='2019-12-01')
    elif request.method == "POST":
        body = request.body

    results = models.Job_result.objects.all()
    data = {'result_list':results}
    return render(request,"job_result_page.html",data)

def job_result_select(request):
    results = models.Job_result.objects.all()
    data = {'result_list':results}
    return render(request,"job_result_page.html",data)

#仅支持一个job跑一个suite
def excute_job_immediately(request,project):
    #获取执行suite时的环境,在setting中配置
    httprunner_project_path = settings.HTTPRUNNER_PROJECT_PATH[project]
    print("httprunner_project_path:",httprunner_project_path)
    suite_path = httprunner_project_path + '\\testsuites\\'

    #获取project相关的suite
    project_obj = models.Project.objects.filter(project_code=project,effective_flag=1)[0]
    suite_dic = project_obj.suite_set.filter(effective_flag=1,status=1).values("suite_name")
    suite_list =[]
    for i in suite_dic:
        suite_list.append(suite_path + i["suite_name"])

    #执行suite并返回结果
    result = myFunctions.run_httprunnner_script(suite_list[0])

    report_path = result['reportpath']
    start_time = result['time']['start_datetime']
    summary = result['stat']['testcases']
    result_name = project +'项目' + start_time +"部署完成触发执行的job"

    #将结果放入表中
    project_obj = models.Project.objects.filter(project_code=project)[0]
    models.Job_result.objects.create(result_name=result_name,project=project_obj,
                                     execute_by=3,executed_result=summary,
                                     link_for_result=report_path,time_start_excute=start_time)

    return HttpResponse("添加成功")



#新建一个定时任务(调试版)
def create_cron_job(request):
    message = None
    project_obj = models.Project.objects.filter(project_code='baidu')[0]
    job_name = '测试job名称'+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #开始执行时间
    time_start_excute = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    iterval_time = 10

    #限制最多执行多少次，是为了限制生成的子任务的个数。
    maximum_times = 1

    if maximum_times<=0:
        message = "最大执行次数必须是大于等于1的整数"
        return HttpResponse(message)
    #开始时间必须大于当前时间

    models.CronJob.objects.create(project=project_obj,job_name=job_name,
                                  time_start_excute=time_start_excute,iterval_time=iterval_time,
                                  maximum_times=maximum_times)

    return HttpResponse("OK")


#启动一个定时任务,新建子任务
def start_cronjob_view(request,job_id):
    try:
        #获取到任务表数据
        job_obj = models.CronJob.objects.filter(id=job_id,effective_flag=1,enable=0)[0]
    except Exception as e:
        return HttpResponse("请检查数据是否符合要求")

    #获取任务详细信息
    time_start_excute = job_obj.time_start_excute
    iterval_time = job_obj.iterval_time
    maximum_times = job_obj.maximum_times

    # print("time_start_excute:",time_start_excute)
    # print("iterval_time:",iterval_time)
    # print("maximum_times:",maximum_times)

    #计算每个子任务执行时间
    for i in range(1,maximum_times + 1 ):
        excute_time = time_start_excute + datetime.timedelta(minutes= iterval_time * i)
        # 在子任务表中插入数据
        models.Subtask.objects.create(cronjob=job_obj, time_excepte_excuted=excute_time.strftime("%Y-%m-%d %H:%M:%S"))

    #更新定时任务表的状态
    models.CronJob.objects.filter(id=job_id, effective_flag=1, enable=0).update(enable = 1,status = 2)

    #给出返回值
    return HttpResponse("定时任务已启动!")


def test_run_cronjob(request,id):
    return myFunctions.test_run_cronjob(id)
