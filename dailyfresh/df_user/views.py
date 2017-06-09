#coding=utf-8
from django.shortcuts import render,redirect
from hashlib import sha1
from models import *
from df_goods.models import GoodsInfo
from df_order.models import *
from django.http import JsonResponse,HttpResponseRedirect
from . import user_decorator
from django.core.paginator import Paginator,Page

# Create your views here.


def index(request):
    return render(request, 'df_user/index.html')


def login(request):
    return render(request, 'df_user/login.html')

def register(request):
    return render(request, 'df_user/register.html')

# def register_post(request):
#     userinfo = user()
#     dict = request.POST
#     userinfo.uname = dict.get('user_name')
#     userinfo.upasswd  = dict.get('pwd')
#     userinfo.uemail = dict.get('email')
#     userinfo.save()
#     return redirect('user/login')


# def register_handle(request):
#     post = request.POST
#     uname = post.get('user_name')
#     upwd = post.get('pwd')
#     upwd2 = post.get('cpwd')
#     uemail = post.get('eamil')
#     if upwd !=upwd2:
#         return redirect('register')
#     #密码加密
#     s1 = sha1()
#     s1.update(upwd)
#     upwd3 = s1.hexdigest()
#     #创建对象
#     user=UserInfo()
#     user.uname=uname
#     user.upwd=upwd3
#     user.ueamil=uemail
#     user.save()
#     # 注册成功，转到登陆页面
#     return redirect('login')
def register_handle(request):
    #接收用户输入
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2=post.get('cpwd')
    uemail=post.get('email')
    #判断两次密码
    if upwd!=upwd2:
        return HttpResponseRedirect('/user/register/')
    #密码加密
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()
    #创建对象
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    #注册成功，转到登录页面
    return HttpResponseRedirect('/user/login/')


def register_exist(request):
    uname =request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})


def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'用户登陆','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)


def login_handle(request):
    # 接收请求信息
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    # 根据用户名查找对象
    users = UserInfo.objects.filter(uname=uname)
    print uname
    # 判断：如果位插到则用户名错，如果查找则判断密码是否正确，正确则转到用户中心
    if len(users)==1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            # 成功后删除转向地址，防止以后直接登陆造成的转向
            red.set_cookie('red_url','',max_age=-1)
            # 记住用户名
            if jizhu !=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            context = {'title':'用户登陆','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)
    else:
        context = {'title':'用户登陆','error_name':1,'error_pawd':0,'uname':uname,'upawd':upwd}
        return render(request,'df_user/login.html',context)

# 退出
def logout(request):
    # print '---------------------------'
    request.session.flush()
    return HttpResponseRedirect('/')


# def center_info(request):
#     return render(request, 'df_user/user_center_info.html')


@user_decorator.login
def center_info(request):
    user_email=UserInfo.objects.get(id=request.session['user_id']).uemail
    #最近浏览
    goods_list=[]
    #获取商品的id
    goods_ids=request.COOKIES.get('liulan','')
    if goods_ids!='':
        goods_ids1=goods_ids.split(',')
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context={'title':'用户中心',
             'user_email':user_email,
             'user_name':request.session['user_name'],
             'page_name':1,
             'goods_list':goods_list}
    return render(request,'df_user/user_center_info.html',context)



@user_decorator.login
# def center_order(request,pindex):
#     order_list=OrderInfo.objects.filter(user_id=request.session['user_id']).order_by('-oid')
#     paginator=Paginator(order_list,2)
#     if pindex=='':
#         pindex='1'
#     page=paginator.page(int(pindex))
#     context={'title':'用户中心',
#              'page_name':1,
#              'paginator':paginator,
#              'page':page,
#              }
#
#     return render(request, 'df_user/user_center_order.html',context)
def center_order(request,pindex):
    order_list=OrderInfo.objects.filter(user_id=request.session['user_id']).order_by('-oid')
    paginator=Paginator(order_list,2)
    if pindex=='':
        pindex='1'
    page=paginator.page(int(pindex))

    context={'title':'用户中心',
             'page_name':1,
             'paginator':paginator,
             'page':page,}
    return render(request,'df_user/user_center_order.html',context)

# def center_site(request):
#     return render(request, 'df_user/user_center_site.html')
@user_decorator.login
def center_site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.ucode=post.get('ucode')
        user.utel=post.get('utel')
        user.save()
    context={'title':'用户中心','user':user,'page_name':1}
    return render(request,'df_user/user_center_site.html',context)
