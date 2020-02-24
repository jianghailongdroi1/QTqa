import requests
import json
import logging
from autotest import models
from autotest.models import UserInfo
import json
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse

from django.shortcuts import render_to_response

def project_list(request):
    request.method =='get'
    return render_to_response('project_list.html')


def suite_list(request):
    request.method =='get'
    return render_to_response('suite_list.html')

def task_list(request):
    request.method =='get'
    return render_to_response('task_list.html')

def reports(request):
    request.method =='get'
    return render_to_response('reports.html')

def modify_task(request):
    request.method =='get'
    return render_to_response('modify_task.html')

def task_run_details(request):
    request.method == 'get'
    return render_to_response('task_run_details.html')

def modify_project(request):
    request.method =='get'
    return render_to_response('modify_project.html')

def modify_suite(request):
    request.method =='get'
    return render_to_response('modify_suite.html')


def register(request):
    if request.method == 'POST':
        user_info = UserInfo.objects
        data={}
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        email = request.POST.get('email',None)
        if user_info.filter(username__exact=username).filter(status=1).count() > 0:
            data['code'] = '1001'
            data['msg'] = '该用户名已被注册，请更换用户名！'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        if user_info.filter(email__exact=email).filter(status=1).count() > 0:
            data['code'] = '1002'
            data['msg'] = '邮箱已被其他用户注册，请更换邮箱!'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        user_info.create(username=username, password=password, email=email)
        data['code'] = '200'
        data['msg'] = '注册成功'
        return HttpResponse(json.dumps(data, ensure_ascii=False))
    elif request.method == 'GET':
        return render_to_response("register.html")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {}
        if UserInfo.objects.filter(username__exact=username).filter(password__exact=password).count() == 1:
            data['code'] = '200'
            data['msg'] = '登录成功！'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            data['code'] = '1002'
            data['msg'] = '登录失败, 请检查用户名或者密码'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
    elif request.method == 'GET':
        return render_to_response("login.html")

def report(request,name):
    request.method == 'get'
    return render_to_response('reports/'+ name +'.html')