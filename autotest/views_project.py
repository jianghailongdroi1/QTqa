import datetime,math

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

#新增项目
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

#编辑项目
def edit_project(request):
    if request.method == "POST":
        data = {}
        project_id = request.POST.get('id',None)
        project_code = request.POST.get('project_code',None)
        project_name = request.POST.get('project_name',None)
        description = request.POST.get('description',None)
        #校验必填字段是否为空
        if not all ([id,project_code,project_name]):
            data['code'] = '1001'
            data['msg'] = '必填项为空'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        #校验project_id是否正确
        project_count = models.Project.objects.filter(id = project_id).count()
        if project_count ==0:
            data['code'] = '1002'
            data['msg'] = 'project不存在'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        else:
            #校验project_code不在已有的项目中存在
            if models.Project.objects.filter(project_code =project_code).exclude(id = project_id).count() != 0:
                data['code'] = '1002'
                data['msg'] = 'project_code已存在'
                return HttpResponse(json.dumps(data, ensure_ascii=False))


            models.Project.objects.filter(id = project_id).update( project_code=project_code,
                                          project_name =project_name,description=description,time_updated = datetime.datetime.now()
                                                             )

            data['code'] = '200'
            data['msg'] = '修改成功'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        return render_to_response('add_project.html')

# 删除项目
def delete_project(request):
    if request.method == "POST":
        data = {}
        project_id = request.POST.get('project_id', None)

        # 校验必填字段是否为空
        if not all([project_id]):
            data['code'] = '1001'
            data['msg'] = '必填项为空'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        # 校验project_id是否正确
        project_count = models.Project.objects.filter(id=project_id).count()
        if project_count == 0:
            data['code'] = '1002'
            data['msg'] = 'project不存在'
            return HttpResponse(json.dumps(data, ensure_ascii=False))

        else:
            models.Project.objects.filter(id=project_id, effective_flag=1).delete()
            data['code'] = '200'
            data['msg'] = '删除成功'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        return render_to_response('project_list.html')


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
        current_page = int(request.POST.get('current_page','1'))
        #每页的数据量
        perPageItemNum = int(request.POST.get('perPageItemNum','10'))
        # print("project_id:",project_id)
        print("current_page:",type(current_page))
        print("perPageItemNum:",type(perPageItemNum))
        # return  HttpResponse("kasjdhfkjasdhkjf")

        #查询数据
        pro_objs = None
        if  project_id != None:
            project_objs = models.Project.objects.filter(id=project_id, effective_flag=1)
            if project_objs.count() == 0:
                data['code'] = '1001'
                data['msg'] = '项目不存在'
                return HttpResponse(json.dumps(data, ensure_ascii=False))

            pro_objs = models.Project.objects.filter(id=project_id, effective_flag=1)

        else:
            pro_objs = models.Project.objects.filter(effective_flag=1)

        # 查询总数据量
        count = pro_objs.count()
        # print('=============count:',count)
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

        #返回值中增加总页数字段
        #count为0时，页数为1
        if count == 0:
            total_page_num =1
        else:
            # count不为0时
            total_page_num = math.ceil(count/perPageItemNum)



        data = {'total':count,
                        'total_page_num':total_page_num,
                        'page_num':current_page,
                        'perPageItemNum':perPageItemNum,
                        'rows':data_list}


        return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        #get请求时
        projects = []
        query_pro = Project.objects.all()
        for pro in query_pro:
            projects.append({

                "id": pro.id,
                "project_code": pro.project_code,
                "project_name": pro.project_name,
                "description": pro.description,
                "time_created": str(pro.time_created),
            })
        return JsonResponse(
            {
                "all_projects": projects,
                "msg": "sucess",
                "status": 200
            }
        )




