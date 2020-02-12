import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from autotest import models
from django.conf import settings
from autotest import myFunctions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import logging
logger = logging.getLogger('HttpRunnerManager')
from autotest.models import Project
import json
from django.shortcuts import render_to_response

def add_project(request):
    if request.method == "POST":
        data = {}
        project_code0 = request.POST.get('project_code',None)
        project_name0 = request.POST.get('project_name',None)
        description0 = request.POST.get('description',None)
        if not all ([project_code0,project_name0]):
            data['code'] = '1001'
            data['msg'] = '必填项为空'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        project_code = Project.objects.filter(project_code=project_code0)
        if project_code.count()> 0:
            data['code'] = '1002'
            data['msg'] = '项目编号已存在'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            new = Project(project_code=project_code0, project_name=project_name0, description=description0)
            new.save()
            data['code'] = '200'
            data['msg'] = '添加成功'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
    return render_to_response('add_project.html')


def list(request):
    request.method == "get"
    return render_to_response('project_list.html')
#
# # Create your views here.
# def get_job_result_add_page(request):
#     return render(request,"job_result_add_page.html")

# #调试用
# def job_result_add(request):
#     if request.method == "GET":
#         project_obj = models.Project.objects.filter(id=2)[0]
#         models.Job_result.objects.create(result_name='执行结果3',project = project_obj,execute_by=1,executed_result='执行结果总数',
#                                          link_for_result='weriuweriu',time_start_excute='2019-12-01')
#     elif request.method == "POST":
#         body = request.body
#
#     results = models.Job_result.objects.all()
#     data = {'result_list':results}
#     return render(request, "job_result_page1.0.html", data)
#
# def job_result_select(request,pagenum =1):
#     job_result_list = models.Job_result.objects.all()#查看所有的数据
#     paginator = Paginator(job_result_list, 10)  # 这里的book_list必须是一个集合对象，把所有的书分页，一页有10个
#     print("count:",paginator.count)           #数据总数
#     print("num_pages",paginator.num_pages)    #总页数
#     page_range= paginator.page_range  #页码的列表
#     # page1=paginator.page(1) #第1页的page对象
#     # for i in page1:         #遍历第1页的所有数据对象
#     #     print(i)
#     print(paginator.page(1).object_list)  # 第1页的所有数据
#     page = request.GET.get('page', pagenum)
#     currentPage = int(page)
#
#     #  如果页数十分多时，换另外一种显示方式
#     if paginator.num_pages>30:
#
#         if currentPage-5<1:
#             page_range=range(1,11)
#         elif currentPage+5>paginator.num_pages:
#             page_range=range(currentPage-5,paginator.num_pages+1)
#
#         else:
#             page_range=range(currentPage-5,currentPage+5)
#     else:
#         page_range=paginator.page_range
#
#     try:
#         print(page)
#         job_result_list = paginator.page(page)
#     except PageNotAnInteger:
#         job_result_list = paginator.page(1)
#     except EmptyPage:
#         job_result_list = paginator.page(paginator.num_pages)
#
#     data = {'result_list':job_result_list}
#     data1 = {'result_list':job_result_list,"paginator":paginator,"currentPage":currentPage,"page_range":page_range}
#     # return render(request,"job_result_page1.0.html",data1)
#     return render(request,"job_result_page2.0.html",data1)
#
# #仅支持一个job跑一个suite
# def excute_job_immediately(request,project):
#     #获取执行suite时的环境,在setting中配置
#     httprunner_project_path = settings.HTTPRUNNER_PROJECT_PATH[project]
#     print("httprunner_project_path:",httprunner_project_path)
#     suite_path = httprunner_project_path + '\\testsuites\\'
#
#     #获取project相关的suite
#     project_obj = models.Project.objects.filter(project_code=project,effective_flag=1)[0]
#     suite_dic = project_obj.suite_set.filter(effective_flag=1,status=1).values("suite_name")
#     suite_list =[]
#     for i in suite_dic:
#         suite_list.append(suite_path + i["suite_name"])
#
#     #执行suite并返回结果
#     result = myFunctions.run_httprunnner_script(suite_list[0])
#
#     report_path = result['reportpath']
#     start_time = result['time']['start_datetime']
#     summary = result['stat']['testcases']
#     result_name = project +'项目' + start_time +"部署完成触发执行的job"
#
#     #将结果放入表中
#     project_obj = models.Project.objects.filter(project_code=project)[0]
#     models.Job_result.objects.create(result_name=result_name,project=project_obj,
#                                      execute_by=3,executed_result=summary,
#                                      link_for_result=report_path,time_start_excute=start_time)
#
#     return HttpResponse("添加成功")
#

# #新建一个定时任务(调试版)
# def create_cron_job(request):
#     message = None
#     project_obj = models.Project.objects.filter(project_code='baidu')[0]
#     job_name = '测试job名称'+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     #开始执行时间
#     time_start_excute = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     iterval_time = 10
#
#     #限制最多执行多少次，是为了限制生成的子任务的个数。
#     maximum_times = 1
#
#     if maximum_times<=0:
#         message = "最大执行次数必须是大于等于1的整数"
#         return HttpResponse(message)
#     #开始时间必须大于当前时间
#
#     models.CronJob.objects.create(project=project_obj,job_name=job_name,
#                                   time_start_excute=time_start_excute,iterval_time=iterval_time,
#                                   maximum_times=maximum_times)
#
#     return HttpResponse("OK")


# #启动一个定时任务,新建子任务
# def start_cronjob_view(request,job_id):
#     try:
#         #获取到任务表数据
#         job_obj = models.CronJob.objects.filter(id=job_id,effective_flag=1,enable=0)[0]
#     except Exception as e:
#         return HttpResponse("请检查数据是否符合要求")
#
#     #获取任务详细信息
#     time_start_excute = job_obj.time_start_excute
#     iterval_time = job_obj.iterval_time
#     maximum_times = job_obj.maximum_times
#
#     # print("time_start_excute:",time_start_excute)
#     # print("iterval_time:",iterval_time)
#     # print("maximum_times:",maximum_times)
#
#     #计算每个子任务执行时间
#     for i in range(1,maximum_times + 1 ):
#         excute_time = time_start_excute + datetime.timedelta(minutes= iterval_time * i)
#         # 在子任务表中插入数据
#         models.Subtask.objects.create(cronjob=job_obj, time_excepte_excuted=excute_time.strftime("%Y-%m-%d %H:%M:%S"))
#
#     #更新定时任务表的状态
#     models.CronJob.objects.filter(id=job_id, effective_flag=1, enable=0).update(enable = 1,status = 2)
#
#     #给出返回值
#     return HttpResponse("定时任务已启动!")

#
# def test_run_cronjob(request,id):
#     return myFunctions.test_run_cronjob(id)


def test_function(request):
    return myFunctions.reset_cronjob_status()

#手动执行调用启动subtask表中的子任务
def excute_all_subtasks(request):
    return myFunctions.test_excute_subtasks()
#重构外部冒烟测试接口
def excute_job_by_thirdParty(request,project_code):
    return myFunctions.create_new_subtask(project_code)

#新建job
def create_job(request):
    data = {'code':200,"msg":'success'}
    if request.method == 'POST':

        # 获取入参
        project_id = request.POST.get('project_id',None)
        job_name = request.POST.get('job_name',None)
        suite_list = request.POST.get('suite_list',None)
        description = request.POST.get('description',None)
        job_type = request.POST.get('job_type',None)

        #传入的suite_list是str格式，需进行转化
        if suite_list is not None:
            new_suite_list = []

            for n in  suite_list[1:-1].split(','):
                new_suite_list.append(int(n))

            suite_list = new_suite_list

        #校验
        if not all ([project_id,job_name,job_type]):
            data['code'] = '1001'
            data['msg'] = '必填项为空'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        project_objs = Project.objects.filter(id=project_id)
        if project_objs.count() == 0:
            data['code'] = '1002'
            data['msg'] = '项目不存在'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        #校验suite_id是否存在
        if suite_list !=None:
            for i in suite_list:
                if models.suite.objects.filter(id = i,effective_flag= 1).count() == 0:
                    data['code'] = '1003'
                    data['msg'] = models.suite.objects.filter(id = i).value('suite_name') +'不存在'
                    return HttpResponse(json.dumps(data, ensure_ascii=False))

        if job_type in ('timing_task','instant_task','called_task'):

            if job_type == 'timing_task':
                # 获取入参
                time_start_excute = request.POST.get('time_start_excute', None)
                iterval_time = request.POST.get('iterval_time', None)
                maximum_times = request.POST.get('maximum_times', None)
                # 校验
                if not all([time_start_excute, iterval_time, maximum_times]):
                    data['code'] = '1001'
                    data['msg'] = '必填项为空'
                    return HttpResponse(json.dumps(data, ensure_ascii=False))

                #新建job
                obj = models.CronJob.objects.create(project = project_objs.first(),
                                              job_name = job_name,description=description,
                                              type = job_type,iterval_time = iterval_time,maximum_times =maximum_times,
                                                time_start_excute = time_start_excute
                                                    )
                #job和suite关联
                if suite_list != None:
                    obj.suite_set.set(suite_list)

                return HttpResponse(json.dumps(data, ensure_ascii=False))

            else:
                # 新建job
                obj = models.CronJob.objects.create(project = project_objs.first(),
                                              job_name = job_name,description=description,
                                              type = job_type)
                # job和suite关联
                if suite_list != None:
                    obj.suite_set.set(suite_list)

                return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            data['code'] = '1005'
            data['msg'] = 'job_type错误'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        #请求方式是 get
        return render_to_response('add_task.html')

#编辑job
def edit_job(request):
    data = {'code':200,"msg":'success'}
    if request.method == 'POST':

        # 获取入参
        job_id = request.POST.get('job_id',None)
        job_type = request.POST.get('job_type',None)

        project_id = request.POST.get('project_id',None)
        job_name = request.POST.get('job_name',None)
        suite_list = request.POST.get('suite_list',None)
        description = request.POST.get('description',None)



        #传入的suite_list是str格式，需进行转化
        if suite_list is not None:
            new_suite_list = []

            for n in  suite_list[1:-1].split(','):
                new_suite_list.append(int(n))

            suite_list = new_suite_list

        #校验
        if not all ([job_id,project_id,job_name,job_type]):
            data['code'] = '1001'
            data['msg'] = '必填项为空'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        job_obj = models.CronJob.objects.filter(id = job_id,effective_flag=1)
        if job_obj.count()  == 0:
            data['code'] = '1002'
            data['msg'] = '任务不存在或已删除'
            return HttpResponse(json.dumps(data, ensure_ascii=False))


        project_objs = Project.objects.filter(id=project_id)
        if project_objs.count() == 0:
            data['code'] = '1002'
            data['msg'] = '项目不已存在'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        #校验suite_id是否存在
        if suite_list !=None:
            for i in suite_list:
                if models.suite.objects.filter(id = i,effective_flag= 1).count() == 0:
                    data['code'] = '1003'
                    data['msg'] = models.suite.objects.filter(id = i).value('suite_name') +'不存在'
                    return HttpResponse(json.dumps(data, ensure_ascii=False))

        if job_type in ('timing_task','instant_task','called_task'):

            if job_type == 'timing_task':
                # 获取入参
                time_start_excute = request.POST.get('time_start_excute', None)
                iterval_time = request.POST.get('iterval_time', None)
                maximum_times = request.POST.get('maximum_times', None)
                # 校验
                if not all([time_start_excute, iterval_time, maximum_times]):
                    data['code'] = '1001'
                    data['msg'] = '必填项为空'
                    return HttpResponse(json.dumps(data, ensure_ascii=False))
                #更新job
                models.CronJob.objects.filter(id =job_id).update(project = project_objs.first(),
                                              job_name = job_name,description=description,
                                              type = job_type,iterval_time = iterval_time,maximum_times =maximum_times,
                                                time_start_excute = time_start_excute,
                                                time_updated = datetime.datetime.now())
            else:
                #更新job
                models.CronJob.objects.filter(id =job_id).update(project = project_objs.first(),
                                              job_name = job_name,description=description,
                                              type = job_type,time_updated = datetime.datetime.now(),
                                              iterval_time=0, maximum_times=0,time_start_excute = None)
            #job和suite关联
            if suite_list != None:
                job_obj.first().suite_set.set(suite_list)
            else:
                job_obj.first().suite_set.set([])
        else:
            data['code'] = 1004
            data['msg'] = 'job_type错误！'
    else:
        return render_to_response('add_task.html')

    return HttpResponse(json.dumps(data))

#删除job
def delete_job(request):
    data = {'code':200,"msg":'success'}
    if request.method == 'POST':

        # 获取入参
        job_id = request.POST.get('job_id',None)

        #校验
        job_obj = models.CronJob.objects.filter(id = job_id,effective_flag=1)
        if job_obj.count()  == 0:
            data['code'] = '1001'
            data['msg'] = '任务不存在或已删除'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        #更新job
        models.CronJob.objects.filter(id =job_id).update(effective_flag =0,
                                        time_updated = datetime.datetime.now())

    else:
        return render_to_response('add_task.html')

    return HttpResponse(json.dumps(data))

#查询jobs
def query_jobs(request):
    if request.method == 'POST':
        data = {}
        #获取数据
        #关于查询的入参
        project_id = request.POST.get('project_id',None)

        #关于分页
        #当前页码
        current_page = request.POST.get('current_page','1')
        #每页的数据量
        perPageItemNum = request.POST.get('perPageItemNum','10')

        #查询数据
        job_objs=None
        if  project_id != None:
            project_objs = Project.objects.filter(id=project_id)
            if project_objs.count() == 0:
                data['code'] = '1001'
                data['msg'] = '项目不存在'
                return HttpResponse(json.dumps(data, ensure_ascii=False))

            job_objs = models.CronJob.objects.filter(project_id=project_id, effective_flag=1)

        else:
            job_objs = models.CronJob.objects.filter( effective_flag=1)

        # 查询总数据量
        count = job_objs.count()
        # print('=============count:',count)
        # 查询具体数据
        job_list = job_objs.values('id','project_id','project__project_name',
                                   'job_name','time_start_excute','iterval_time',
                                   'maximum_times','type','status','description',
                                   'enable','time_created','time_updated')
        # print('=============job_list:',job_list)
        jobs = []
        for job in job_list:
            jobs.append(job)
        # print("==============jobs:",jobs)

        #分页
        from autotest.myUtil.pager import Pagination

        page_obj = Pagination(count, current_page,perPageItemNum)

        data_list = jobs[int(page_obj.start()) : int(page_obj.end()) ]

        from autotest.myUtil.commonFunction import turn_dic_to_be_JSON_serializable
        # print("data_list:",data_list)
        for dic in data_list:
            turn_dic_to_be_JSON_serializable(dic)

        data['code'] = 200
        data['msg'] = '操作成功'
        data['data'] = {'total':count,
                        'page_num':current_page,
                        'perPageItemNum':perPageItemNum,
                        'data':data_list}


        return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        return render_to_response('job_list.html')

#查询job的详细信息
def query_job_detail(request):
    if request.method == 'POST':
        data = {}
        #获取数据
        #关于查询的入参
        job_id = request.POST.get('job_id',None)
        job_objs = models.CronJob.objects.filter(id=job_id)

        count = job_objs.count()
        if count == 0:
            data['code'] = '1001'
            data['msg'] = 'job不存在'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        #查询数据
        job_data = models.CronJob.objects.filter(id=job_id).values('id','project_id','project__project_name',
                                   'job_name','time_start_excute','iterval_time',
                                   'maximum_times','type','status','description',
                                   'enable','time_created','time_updated')[0]
        from autotest.myUtil.commonFunction import turn_dic_to_be_JSON_serializable

        job_data  = turn_dic_to_be_JSON_serializable(job_data)

        data['code'] = 200
        data['msg'] = '操作成功'
        data['data'] = job_data

        return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        return render_to_response('job_list.html')

#启动任务,新建子任务
def enable_job(request):
    if request.method == "POST":
        data={}
        # 获取入参
        job_id = request.POST.get('job_id',None)

        #校验
        if not  job_id:
            data['code'] = '1001'
            data['msg'] = 'job_id不能为空'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        job_obj = models.CronJob.objects.filter(id=job_id).first()

        if job_obj.effective_flag == '0':
            data['code'] = '1002'
            data['msg'] = '当前任务已被删除，不能启用'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        if job_obj.enable == '1':
            data['code'] = '1003'
            data['msg'] = '当前任务已被启用，不能重复启用'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        #判断任务下是否有对应的suite，没有就报错
        suite_count = models.CronJob.objects.get(id=job_id).suite_set.all().count()
        if suite_count ==0:
            data['code'] = '1004'
            data['msg'] = '请先关联suite'
            return HttpResponse(json.dumps(data, ensure_ascii=False))


        job_type = job_obj.type
        #第三方调用任务
        if job_type == 'called_task':
            if job_obj.enable == '0':
                models.CronJob.objects.filter(id=job_id,effective_flag=1).update(enable=1, status=2
                                                                                 ,time_updated=datetime.datetime.now())

                data['code'] = '200'
                data['msg'] = '第三方调用任务启动成功'

                #给出返回值
                return HttpResponse(json.dumps(data, ensure_ascii=False))
            else:
                models.CronJob.objects.filter(id=job_id ,effective_flag=1).update(enable=1,time_updated=datetime.datetime.now())
                data['code'] = '200'
                data['msg'] = '第三方调用任务恢复启动状态'
                #给出返回值
                return HttpResponse(json.dumps(data, ensure_ascii=False))

        #定时任务
        if job_type == 'timing_task':
            if job_obj.enable == '0':
                #获取任务详细信息
                time_start_excute = job_obj.time_start_excute
                iterval_time = job_obj.iterval_time
                maximum_times = job_obj.maximum_times

                #计算每个子任务执行时间
                for i in range(1,maximum_times + 1 ):
                    excute_time = time_start_excute + datetime.timedelta(minutes= iterval_time * i)
                    # 在子任务表中插入数据
                    models.Subtask.objects.create(cronjob=job_obj, time_excepte_excuted=excute_time.strftime("%Y-%m-%d %H:%M:%S"))

                #更新定时任务表的状态
                models.CronJob.objects.filter(id=job_id).update(enable = 1,status = 2,time_updated=datetime.datetime.now())

                data['code'] = '200'
                data['msg'] = '定时任务启动成功'

                #给出返回值
                return HttpResponse(json.dumps(data, ensure_ascii=False))
            else:
                # 更新定时任务表的状态
                models.CronJob.objects.filter(id=job_id).update(enable=1,time_updated=datetime.datetime.now())

                data['code'] = '200'
                data['msg'] = '定时任务恢复启动状态'

                #给出返回值
                return HttpResponse(json.dumps(data, ensure_ascii=False))

        #立即执行任务
        if job_type == 'instant_task':
            if job_obj.enable == '0':
                #获取任务详细信息
                time_start_excute = job_obj.time_start_excute

                # 在子任务表中插入数据
                models.Subtask.objects.create(cronjob=job_obj, time_excepte_excuted=datetime.datetime.now())

                #更新定时任务表的状态
                models.CronJob.objects.filter(id=job_id).update(enable = 1,status = 2,time_updated=datetime.datetime.now())

                data['code'] = '200'
                data['msg'] = '即时任务启动成功'
                #给出返回值
                return HttpResponse(json.dumps(data, ensure_ascii=False))
            else:
                # 更新定时任务表的状态
                models.CronJob.objects.filter(id=job_id).update(enable=1,time_updated=datetime.datetime.now())

                data['code'] = '200'
                data['msg'] = '即时任务恢复启动状态'

                #给出返回值
                return HttpResponse(json.dumps(data, ensure_ascii=False))

#暂停任务,仅将enable置为2
def unenable_job(request):
    if request.method == "POST":
        data={}
        # 获取入参
        job_id = request.POST.get('job_id',None)

        #校验
        if not  job_id:
            data['code'] = '1001'
            data['msg'] = 'job_id不能为空'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        job_obj = models.CronJob.objects.filter(id=job_id).first()

        if job_obj.effective_flag == '0':
            data['code'] = '1002'
            data['msg'] = '当前任务已被删除，不能暂停'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        if job_obj.enable != '1':
            data['code'] = '1003'
            data['msg'] = '当前任务不是启用状态，不能暂停'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        # 更新定时任务表的状态
        models.CronJob.objects.filter(id=job_id).update(enable=2, time_updated=datetime.datetime.now())

        data['code'] = '200'
        data['msg'] = '任务已暂停！'

        return HttpResponse(json.dumps(data, ensure_ascii=False))


#新建suite
def add_suite(request):
    if request.method == "POST":
        data = {}
        project_id = request.POST.get('project_id',None)
        suite_name = request.POST.get('suite_name',None)
        description = request.POST.get('description',None)
        if not all ([project_id,suite_name]):
            data['code'] = '1001'
            data['msg'] = '必填项为空'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        project_obj = Project.objects.filter(id=project_id)
        if project_obj.count() == 0:
            data['code'] = '1002'
            data['msg'] = '项目不存在'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            suite_obj = models.suite(project_id=project_id, suite_name=suite_name, description=description)
            suite_obj.save()
            data['code'] = '200'
            data['msg'] = '添加成功'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        return render_to_response('add_suite.html')

#删suite
def delete_suite(request):
    if request.method == "POST":
        data = {}
        suite_id = request.POST.get('suite_id',None)

        suite_count = models.suite.objects.filter(id = suite_id).count()
        if suite_count ==0:
            data['code'] = '1001'
            data['msg'] = 'suite不存在'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        else:
            models.suite.objects.filter(id =suite_id).update(effective_flag = 0,time_updated = datetime.datetime.now()
                                                             )

            data['code'] = '200'
            data['msg'] = '删除成功'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        return render_to_response('suite_list.html')

#编辑suite
def edit_suite(request):
    if request.method == "POST":
        data = {}
        suite_id = request.POST.get('suite_id',None)
        project_id = request.POST.get('project_id',None)
        suite_name = request.POST.get('suite_name',None)
        description = request.POST.get('description',None)
        if not all ([suite_id,project_id,suite_name]):
            data['code'] = '1001'
            data['msg'] = '必填项为空'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        suite_count = models.suite.objects.filter(id = suite_id).count()
        if suite_count ==0:
            data['code'] = '1002'
            data['msg'] = 'suite不存在'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        project_obj = Project.objects.filter(id=project_id)
        if project_obj.count() == 0:
            data['code'] = '1003'
            data['msg'] = '项目不存在'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            models.suite.objects.filter(id =suite_id).update(project_id=project_id, suite_name=suite_name,
                                     description=description,time_updated = datetime.datetime.now()
                                                             )

            data['code'] = '200'
            data['msg'] = '修改成功'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        return render_to_response('suite_list.html')

#查询 执行结果
def query_job_results(request):
    if request.method == 'POST':
        data = {}
        #获取数据
        #关于查询的入参
        project_id = request.POST.get('project_id',None)
        job_id = request.POST.get('job_id',None)

        #关于分页
        #当前页码
        current_page = request.POST.get('current_page','1')
        #每页的数据量
        perPageItemNum = request.POST.get('perPageItemNum','10')

        #先设置一个变量，用于放置结果对象的QuerySet[]
        result_objs = None

        #project_id不为空
        if  project_id != None:
            #判断project_id是否有效
            if models.Project.objects.filter(id = project_id,effective_flag= 1).count() == 0:
                data['code'] = '1001'
                data['msg'] = '项目不存在或无效'
                return HttpResponse(json.dumps(data, ensure_ascii=False))

            #job_id也不为空
            if job_id != None:
                #判断job_id是否存在
                if models.CronJob.objects.filter(id = job_id,effective_flag= 1).count() == 0:
                    data['code'] = '1001'
                    data['msg'] = '任务不存在或无效'
                    return HttpResponse(json.dumps(data, ensure_ascii=False))

                result_objs = models.Job_result.objects.filter(project_id =project_id ,cronjob_id= job_id)
            else:
                #job_id为空
                result_objs = models.Job_result.objects.filter(project_id=project_id)
        else:
            #project_id为空
            #job_id不为空
            if job_id != None:
                #判断job_id是否存在
                if models.CronJob.objects.filter(id = job_id,effective_flag= 1).count() == 0:
                    data['code'] = '1001'
                    data['msg'] = '任务不存在或无效'
                    return HttpResponse(json.dumps(data, ensure_ascii=False))

                result_objs = models.Job_result.objects.filter(cronjob_id= job_id)
            else:
                #job_id为空
                result_objs = models.Job_result.objects.all()

        # 查询总数据量
        count = result_objs.count()
        # print('=============count:',count)
        # 查询具体数据
        result_list = result_objs.values('id','project__project_name','cronjob__job_name',
                                   'executed_result','link_for_result','time_start_excute',
                                   'time_end_excute','cronjob__type')
        # print('=============job_list:',result_list)
        results = []
        for result in result_list:
            results.append(result)

        #分页
        from autotest.myUtil.pager import Pagination

        page_obj = Pagination(count, current_page,perPageItemNum)

        data_list = results[int(page_obj.start()) : int(page_obj.end()) ]

        from autotest.myUtil.commonFunction import turn_dic_to_be_JSON_serializable
        # print("data_list:",data_list)
        for dic in data_list:
            turn_dic_to_be_JSON_serializable(dic)

        data['code'] = 200
        data['msg'] = '操作成功'
        data['data'] = {'total':count,
                        'page_num':current_page,
                        'perPageItemNum':perPageItemNum,
                        'data':data_list}


        return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        return render_to_response('job_list.html')

#查询project
def SearchForProject(request):
    # return HttpResponse("asdjhflkajsdklf")
    if request.method == 'POST':
        data = {}
        #获取数据
        #关于查询的入参
        project_id = request.POST.get('project_id',None)

        #关于分页
        #当前页码
        current_page = request.POST.get('current_page','1')
        #每页的数据量
        perPageItemNum = request.POST.get('perPageItemNum','10')
        print("project_id:",project_id)
        print("current_page:",current_page)
        print("perPageItemNum:",perPageItemNum)
        # return  HttpResponse("kasjdhfkjasdhkjf")

        #查询数据
        pro_objs=None
        if  project_id != None:
            project_objs = models.Project.objects.filter(project_id=project_id, effective_flag=1)
            if project_objs.count() == 0:
                data['code'] = '1001'
                data['msg'] = '项目不存在'
                return HttpResponse(json.dumps(data, ensure_ascii=False))

            # pro_objs = models.CronJob.objects.filter(project_id=project_id, effective_flag=1)

        else:
            pro_objs = models.Project.objects.filter( effective_flag=1)

        # 查询总数据量
        count = pro_objs.count()
        print('=============count:',count)
        # 查询具体数据
        pro_list = pro_objs.values('id','project_code','project_name',
                                   'description','time_created','time_updated')
        pros = []
        for pro in pro_list:
            pros.append(pro)

        #分页
        from autotest.myUtil.pager import Pagination

        page_obj = Pagination(count, current_page,perPageItemNum)

        data_list = pros[int(page_obj.start()) : int(page_obj.end()) ]

        from autotest.myUtil.commonFunction import turn_dic_to_be_JSON_serializable
        # print("data_list:",data_list)
        for dic in data_list:
            turn_dic_to_be_JSON_serializable(dic)

        data['code'] = 200
        data['msg'] = '操作成功'
        data['data'] = {'total':count,
                        'page_num':current_page,
                        'perPageItemNum':perPageItemNum,
                        'data':data_list}


        return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        return render_to_response('job_list.html')

#查询suite
def SearchForSuite(request):
    if request.method == 'POST':
        data = {}
        #获取数据
        #关于查询的入参
        project_id = request.POST.get('project_id',None)

        #关于分页
        #当前页码
        current_page = request.POST.get('current_page','1')
        #每页的数据量
        perPageItemNum = request.POST.get('perPageItemNum','10')
        # print("project_id:",project_id)
        # print("current_page:",current_page)
        # print("perPageItemNum:",perPageItemNum)


        #查询数据
        suit_objs=None
        if  project_id != None:
            project_objs = models.suite.objects.filter(project_id=project_id, effective_flag=1)
            if project_objs.count() == 0:
                data['code'] = '1001'
                data['msg'] = 'suite不存在'
                return HttpResponse(json.dumps(data, ensure_ascii=False))

            # pro_objs = models.CronJob.objects.filter(project_id=project_id, effective_flag=1)

        else:
            pro_objs = models.suite.objects.filter( effective_flag=1)

        # 查询总数据量
        count = pro_objs.count()
        print('=============count:',count)
        # 查询具体数据
        suit_list = pro_objs.values('id','project_id','suite_name',
                                   'description','time_created')
        suits = []
        for suit in suit_list:
            suits.append(suit)

        #分页
        from autotest.myUtil.pager import Pagination

        page_obj = Pagination(count, current_page,perPageItemNum)

        data_list = suits[int(page_obj.start()) : int(page_obj.end()) ]

        from autotest.myUtil.commonFunction import turn_dic_to_be_JSON_serializable
        # print("data_list:",data_list)
        for dic in data_list:
            turn_dic_to_be_JSON_serializable(dic)

        data['code'] = 200
        data['msg'] = '操作成功'
        data['data'] = {'total':count,
                        'page_num':current_page,
                        'perPageItemNum':perPageItemNum,
                        'data':data_list}


        return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        return render_to_response('job_list.html')




