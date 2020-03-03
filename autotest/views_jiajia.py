import requests
import json
import logging
from autotest import models
from autotest.models import UserInfo,VerifyCode
import json
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.shortcuts import render,redirect,HttpResponse
import random
from django.core.mail import send_mail   # 导入邮箱模块

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

def verifycode(randomlength=8):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def forgetpwd(request):
    data = {}
    codeObj = VerifyCode.objects
    if request.method=="GET":
        email = request.GET.get("email")
        email_title = "找回密码"
        code = verifycode()#随机生成的验证码
        if codeObj.filter(email = email).count()<1:
            codeObj.create(email=email,code = code,status = 1)
        else:
            codeObj.filter(email=email).update(code=code,status=1)
        # request.session["code"]=code #将验证码保存到session
        email_body = "验证码为：{0}".format(code)
        send_status = send_mail(email_title, email_body,"790049767@qq.com",[email],fail_silently=False)
        data['code'] = "200"
        data['msg']="验证码已发送，请查收邮件"
        return HttpResponse(json.dumps(data,ensure_ascii=False))
    else:
        email =  request.POST.get("email")
        password = request.POST.get("password")
        code = request.POST.get("code") #获取传递过来的验证码
        # 判断验证码是否一致
        if codeObj.filter(email = email).filter(status=1).count() >= 1:
            if code == codeObj.get(email = email).code:
                UserInfo.objects.filter(email=email).update(password=password)
                codeObj.filter(email=email).update(status = 0)
                data['code'] = '200'
                data['msg'] = '密码已重置，快去登录吧'
                return HttpResponse(json.dumps(data, ensure_ascii=False))
            else:
                data['code'] = '1001'
                data['msg'] = '验证码错误'
                return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            data['code'] = '1002'
            data['msg'] = '请先获取验证码'
        return HttpResponse(json.dumps(data, ensure_ascii=False))


def is_login(func):
    def inner(request,*args,**kwargs):
        if request.session.get("username",default=None):
            ret = func(request,*args,**kwargs)
            return ret
        else:
            return redirect("/autotest/2/login/")
    return inner

@is_login
def loginout(request):
    request.method = "POST"
    request.session.flush()
    data={}
    data['code'] = '200'
    data['msg'] = '退出成功！'
    return HttpResponse(json.dumps(data, ensure_ascii=False))

@is_login
def html(request,name):
    request.method == 'get'
    return render_to_response(name + '.html')

@is_login
def report(request,name):
    request.method == 'get'
    return render_to_response('reports/'+ name +'.html')