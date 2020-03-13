import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from autotest import models
from django.conf import settings
from autotest import myFunctions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# import logging
# logger = logging.getLogger('HttpRunnerManager')
from autotest.models import Project
import json,math
from django.shortcuts import render_to_response




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
            #判断suite_list为'[]',即为空的情况
            if suite_list == '[]':
                suite_list = None
            else:
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
            #判断suite_list为'[]',即为空的情况
            if suite_list == '[]':
                suite_list = None
            else:
                new_suite_list = []
                for n in  suite_list[1:-1].split(','):
                    new_suite_list.append(int(n))

                suite_list = new_suite_list

        #校验
        if not all ([project_id,job_name,job_type]):
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
        current_page = int(request.POST.get('current_page','1'))
        #每页的数据量
        perPageItemNum = int(request.POST.get('perPageItemNum','10'))

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

        #返回值中增加总页数字段
        #count为0时，页数为1
        if count == 0:
            total_page_num =1
        else:
            # count不为0时
            total_page_num = math.ceil(count/perPageItemNum)
        data = {'total':count,
                        'total_page_num': total_page_num,
                        'page_num':current_page,
                        'perPageItemNum':perPageItemNum,
                        'rows':data_list}


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
        job_obj = models.CronJob.objects.get(id=job_id)
        suites =job_obj.suite_set.filter(effective_flag= 1).values('id','suite_name')
        suite_list = []
        for suite in suites:
            suite_list.append(suite)

        from autotest.myUtil.commonFunction import turn_dic_to_be_JSON_serializable

        job_data  = turn_dic_to_be_JSON_serializable(job_data)
        job_data['suite_list']=suite_list

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





