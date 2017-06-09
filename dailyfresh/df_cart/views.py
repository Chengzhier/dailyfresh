# coding=utf-8
from django.http import HttpResponse, JsonResponse, HttpRequest
# from df_user.user_decorator import *
from df_user import user_decorator
from models import *
# import df_user.user_decorator
from django.shortcuts import render,redirect
# Create your views here.


@user_decorator.login
# 添加商品到购物车
def add(request,gid,count):

    carts=CartInfo.objects.filter(goods_id=gid).filter(user_id=request.session['user_id'])
    if len(carts)==0:
        cart=CartInfo()
        cart.goods_id=int(gid)
        cart.user_id=request.session['user_id']
        cart.count=int(count)
        cart.save()
    else:
        cart=carts[0]
        cart.count+=int(count)
        cart.save()
    if request.is_ajax():
        return JsonResponse({'count':CartInfo.objects.filter(user_id=request.session['user_id']).count()})
    else:
        return redirect('/cart/')


@user_decorator.login
def carts(request):
    # return HttpResponse('ok')
    cart_list=CartInfo.objects.filter(user_id=int(request.session['user_id']))
    context={
        'title':'购物车',
        'page_name':1,
        'cart_list':cart_list,
    }
    return render(request,'df_cart/cart.html',context)

def count_change(request):
    id=request.GET.get('id')
    count=request.GET.get('count')
    cart=CartInfo.objects.get(id=int(id))
    cart.count=int(count)
    return JsonResponse({'count':cart.count})

def delete(request):
    id=request.GET.get('id')
    cart=CartInfo.objects.get(id=int(id))
    cart.delete()
    return JsonResponse({'result':'ok'})

def order(request):
    user=UserInfo.objects.get(id=request.session['user_id'])
    cart_ids=request.GET.getlist('cart_id')
    carts=CartInfo.objects.filter(id__in=cart_ids)
    context={
        'title':'提交订单',
        'page_name':1,
        'user':user,
        'carts':carts,
    }
    return render(request,'df_cart/order.html',context)




