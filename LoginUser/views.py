from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from .models import *
import hashlib
from django.core.paginator import Paginator
import random
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
                    respose.set_cookie('userid',user.id)
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


def base(request):

    return render(request,'base.html')

def add_goods(request):
    goods_name = '冬瓜，苦瓜，乳瓜，黄瓜，丝瓜，佛手瓜，菜瓜，胡瓜，瓠瓜、菜瓜、西葫芦，番茄，茄子，芸豆，豇豆，豌豆，架豆，刀豆，扁豆，青豆，毛豆，蛇豆，玉米，玉米尖，蚕豆、菜豆、眉豆、四棱豆、蛇瓜，菌类：木耳，银耳，地耳，石耳，平菇，草菇，口蘑，猴头菇，金针菇，香菇，鸡腿菇，竹荪，凤尾菇，茶树菇，杏鲍菇，秀珍菇，猪肚菇，裙带菜瓜类：西瓜，美人瓜，甜瓜，香瓜，黄河蜜，哈密瓜，木瓜，乳瓜'
    goods_name =goods_name.split("，")
    goods_address = "北京市，天津市，上海市，重庆市，河北省，山西省，辽宁省，吉林省，黑龙江省，江苏省，浙江省，安徽省，福建省，江西省，山东省，河南省，湖北省，湖南省，广东省，海南省，四川省，贵州省，云南省，陕西省，甘肃省，青海省，台湾省，内蒙古自治区，广西壮族自治区，西藏自治区，宁夏回族自治区，新疆维吾尔自治区，香港特别行政区，澳门特别行政区"
    goods_address = goods_address.split("，")
    # print(goods_address)
    for i,j in enumerate(range(100),1):
        goods = Goods()
        # print(goods)
        # goods.goods_number = str(i).zfill(5)
        # goods.goods_name = random.choice(goods_address) + random.choice(goods_name)
        # goods.goods_price = random.random()*100
        # goods.goods_count = random.randint(1,10)
        # goods.goods_location = random.choice(goods_address)
        # goods.goods_safe_data = random.randint(1,36)
        # goods.save()
    return HttpResponse('数据已添加')
def goods_list(request,status,page=1):
    #分页
    page=int(page)
    if status=="0":
        goods_list = Goods.objects.filter(goods_status=0).order_by("goods_number")
    else:
        goods_list = Goods.objects.filter(goods_status=1).order_by("goods_number")
    goods_list = Paginator(goods_list,10)
    page=goods_list.page(page)


    # return render(request,"goods_list.html",locals())
    return  render(request,'vue_goods_list.html')
def goods_status(request,status,id):
    """
    完成下架 修改status为0
    完成上架 修改status为1

    :param request:
    :param status: 操作内容 上架
    :param id: 商品 id
    :return:
    """
    id= int(id)
    goods=Goods.objects.get(id=id)
    if status== 'up':
        ###上架
        goods.goods_status = 1
    else:
        #下架
        goods.goods_status = 0
    goods.save()
    url =request.META.get("HTTP_REFERER",'/goods_list/1/1/')
    return HttpResponseRedirect(url)
def goods_list_api(request,status,page=1):
    #分页
    page=int(page)
    if status=="0":
        #下架商品
        goods_list = Goods.objects.filter(goods_status=0).order_by("goods_number")
    else:
        # 在售商品
        goods_list = Goods.objects.filter(goods_status=1).order_by("goods_number")
    goods_list = Paginator(goods_list,10)
    page=goods_list.page(page)

    res=[]
    for one in page:
        res.append({
            "goods_number":one.goods_number,
            "goods_name":one.goods_name,
            "goods_price":one.goods_price,
            "goods_count":one.goods_count,
            "goods_location":one.goods_location,
            "goods_safe_data":one.goods_safe_data,
            "goods_status":one.goods_status,
            "goods_pro_time":one.goods_pro_time,

        })
    # return render(request,"goods_list.html",locals())
    result={
        "data":res,
        "page_range":list(goods_list.page_range),
    }
    return JsonResponse(result)

def api(request):

    return render(request,'api.html')

def vuedemo(request):

    return render(request,"vuedemo.html")

from django.views import View
###类视图
import json
class GoodView(View):
    #处理请求 get post put delete
    #廷议返回的格式，重写init方法
    def __init__(self):
        super(GoodView,self).__init__()
        #构造返回的格式
        self.result = {
            "vsrsion":"v1.0",
            "code":200,
            "data":""
        }
        self.obj =Goods
    def get(self,request):
        #处理get请求
        # return JsonResponse({"methods":"get"})
        # result = self.result
        # result["data"]='get请求'
        id = request.GET.get("id")
        if id:
            #查询指定id的商品
            goods = self.obj.objects.get(id=id)
            data = {
                "goods_number": goods.goods_number,
                "goods_name": goods.goods_name,
                "goods_price": goods.goods_price,
                "goods_count": goods.goods_count,
                "goods_location": goods.goods_location,
                "goods_safe_data": goods.goods_safe_data,
                "goods_pro_time": goods.goods_pro_time,
            }
        else:
            goods = self.obj.objects.all()
            data = []
            for one in goods:
                #one 是一个objects
                data.append({
                    "goods_number":one.goods_number,
                    "goods_name":one.goods_name,
                    "goods_price":one.goods_price,
                    "goods_count":one.goods_count,
                    "goods_location":one.goods_location,
                    "goods_safe_data":one.goods_safe_data,
                    "goods_pro_time":one.goods_pro_time,
                })
        self.result['data']=data
        return JsonResponse(self.result)
    def post(self,request):

        """
        处理post请求
        用来保存数据
        :param request:
        :return:
        """
        data = request.POST
        goods = self.obj()
        goods.goods_number = data.get("goods_number")
        goods.goods_name = data.get("goods_name")
        goods.goods_price = data.get("goods_price")
        goods.goods_count = data.get("goods_count")
        goods.goods_location = data.get("goods_location")
        goods.goods_safe_data = data.get("goods_safe_data")
        goods.goods_pro_time = data.get("goods_pro_time")
        goods.goods_status = data.get("goods_status")
        goods.save()
        self.result['data']={
            "id":goods.id,
            "data":"保存成功",
        }
        return JsonResponse(self.result)

    def put(self,request):
        """
        处理put请求
        更新数据
        更新指定id的商品名字

        :param request:
        :return:
        """
        data =json.loads(request.body.decode())
        print(data)
        id = data.get('id')
        goodsname = data.get('goodsname')
        goods = self.obj.objects.get(id=id)
        goods.goods_name = goodsname
        goods.save()
        self.result['data'] = {
            "id":id,
            "data":'商品名字更新成功'
        }
        return JsonResponse(self.result)
        pass

    def delete(self,request):
        # 处理delete请求
        data = json.loads(request.body.decode())
        id = data.get("id")
        self.obj.objects.filter(id=id).delete()
        self.result["data"] = {
            "id":id,
            "data":"商品删除成功"
        }
        return JsonResponse(self.result)


from rest_framework import viewsets
from LoginUser.serializer import *
class GoodsViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all() ##queryset  固定写法
    serializer_class = GoodsSerializers ###

@LoginVaild
def personal_info(request):
    ##
    user_id =request.COOKIES.get("userid")
    print(user_id)
    user = LoginUser.objects.filter(id=user_id).first()
    if request.method == "POST":
        data = request.POST
        print(data.get('email'))
        user.username = data.get("username")
        user.phone_number=data.get("phone_number")
        user.age=data.get("age")
        user.gender=data.get("gender")
        user.address=data.get("address")
        user.photo=request.FILES.get("photo")
        user.save()
        print(data)
    return render(request,"personal_info.html",locals())
