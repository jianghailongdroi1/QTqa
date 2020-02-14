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
            #根据project_id查询对应的项目
            project_objs = models.Project.objects.filter(id=project_id, effective_flag=1)
            #项目不存在时报错
            if project_objs.count() == 0:
                data['code'] = '1001'
                data['msg'] = 'project_id不正确'
                return HttpResponse(json.dumps(data, ensure_ascii=False))

            #项目存在时，按照project_id来查询对应的suite
            suite_objs = models.suite.objects.filter(project_id=project_id, effective_flag=1)

        else:
            #入参中没有project_id
            suite_objs = models.suite.objects.filter( effective_flag=1)

        # 查询总数据量
        count = suite_objs.count()
        print('=============count:',count)
        # 查询具体数据
        suit_list = list(suite_objs.values('id','project_id','project__project_name','suite_name',
                                   'description','time_created'))

        #分页
        from autotest.myUtil.pager import Pagination

        page_obj = Pagination(count, current_page,perPageItemNum)

        data_list = suit_list[int(page_obj.start()) : int(page_obj.end()) ]

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
        return  render_to_response('suite_list.html')


#查询根据project_id查询suite列表，并且不分页
def SearchForSuite_by_project_id(request):
    if request.method == 'POST':
        data = {}
        #获取数据
        #关于查询的入参
        project_id = request.POST.get('project_id',None)


        #查询数据
        if  project_id != None:
            project_objs = models.suite.objects.filter(id=project_id, effective_flag=1)
            if project_objs.count() == 0:
                data['code'] = '1006'
                data['msg'] = '选择的项目不存在或已删除'
                return HttpResponse(json.dumps(data, ensure_ascii=False))

            suite_objs = models.suite.objects.filter(project_id=project_id, effective_flag=1)

        else:
            suite_objs = models.suite.objects.filter( effective_flag=1)

        # 查询总数据量
        count = suite_objs.count()
        # print('=============count:',count)
        # 查询具体数据
        suit_list = list(suite_objs.values('id','project_id','project__project_name','suite_name',
                                   'description','time_created'))

        from autotest.myUtil.commonFunction import turn_dic_to_be_JSON_serializable

        for dic in suit_list:
            turn_dic_to_be_JSON_serializable(dic)

        data['code'] = 200
        data['msg'] = '操作成功'
        data['data'] = {'total':count,
                        'data':suit_list}

        return HttpResponse(json.dumps(data, ensure_ascii=False))


