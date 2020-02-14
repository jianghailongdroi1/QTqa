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
