from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import LoginUser
import hashlib
def register(request):
    if request.method=="POST":
        error_msg=''
        email= request.POST.get('email')
        password=request.POST.get('password')
        if email:
            #判断邮箱是否存在
            loginuser = LoginUser.objects.filter(email=email).first()
            if not loginuser:
                ##不存在 写库
                user = LoginUser()
                user.username = email
                user.email = email
                user.password = SetPassword(password)
                user.save()
            else:
                error_msg="邮箱也注册"
        else:
            error_msg = '邮箱不可以为空'
    return render(request,'register.html',locals())

# Create your views here.
def login(request):
    if request.method=="POST":
        error_msg=''
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email:
            user = LoginUser.objects.filter(email=email).first()
            if user:
                if user.password == SetPassword(password):
                    respose = HttpResponseRedirect('/index/')
                    respose.set_cookie('username',user.username)
                    request.session['username'] = user.username
                    return respose
                else:
                    error_msg = '密码不正确'
            else:
                error_msg = '用户不存在'
        else:
            error_msg='用户邮箱不能为空'

    return render(request,'login.html',locals())
def SetPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result
def forgot(request):

    return render(request,'forgot.html')

#装饰器
def LoginVaild(func):
    #获取cookie中的username和email
    #判断username和email
    #如果成功 跳转
    #如果失败 login.html
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get('username')
        print(username)
        #获取session
        session_username = request.session.get('username')
        print(session_username)
        if username and session_username and username == session_username:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner

@LoginVaild
def index(requset):

    return render(requset,'index.html')
def logout(request):
    # 登入
    response = HttpResponseRedirect('/login/')
    keys = request.COOKIES.keys()
    for one in keys:
        response.delete_cookie(one)
    del request.session['usrname']
    return response