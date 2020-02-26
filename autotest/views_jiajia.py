import requests
import json
import logging
from autotest import models
from autotest.models import UserInfo
import json
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.shortcuts import render,redirect,HttpResponse

from django.shortcuts import render_to_response

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
            request.session['username'] = username
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            data['code'] = '1002'
            data['msg'] = '登录失败, 请检查用户名或者密码'
            return HttpResponse(json.dumps(data, ensure_ascii=False))
    elif request.method == 'GET':
        return render_to_response("login.html")



def is_login(func):
    def inner(request,*args,**kwargs):
        if request.session.get("username",default=None):
            ret = func(request,*args,**kwargs)
            return ret
        else:
            return redirect("/login/")
    return inner

@is_login
def html(request,name):
    request.method == 'get'
    return render_to_response(name + '.html')

@is_login
def report(request,name):
    request.method == 'get'
    return render_to_response('reports/'+ name +'.html')