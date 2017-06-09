# coding=utf-8
from django.shortcuts import render,redirect
from django.db import transaction
from df_goods.models import GoodsInfo
from df_cart.models import CartInfo
from datetime import datetime

from models import *

# Create your views here.

@transaction.atomic
def order(request):
    post=request.POST
    address=post.get('address')
    cart_id=post.getlist('cart_id')
    # 保存点
    sid=transaction.savepoint()


    # 捕获异常
    try:
        #1
        # 新建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.oaddress = address
        order.ototal = 0
        order.save()
        # 创建订单对象
        # cart_ids1 = [int(item) for item in cart_id.split(',')]
        #计算总金额
        total = 0
        #判断购物车中商品的库存
        for cid in cart_id:
            cart=CartInfo.objects.get(pk=cid)
            if cart.goods.gkucun>=cart.count:
                #库存足够，可以购买
                #减少库存量
                cart.goods.gkucun-=cart.count
                cart.goods.save()
                #将信息加入详单
                detail=OrderDetailInfo()
                detail.order=order
                detail.goods=cart.goods
                detail.price=cart.goods.gprice
                detail.count=cart.count
                detail.save()
                total+=cart.goods.gprice*cart.count
                #删除购物车数据
                cart.delete()
            else:
                #库存不足，不能购买
                transaction.savepoint_rollback(sid)
                return redirect('/cart/')
            #保存总计
        order.ototal=total
        order.save()

            #2
            #3
            #4
            #5
        # 如果没问题就提交（提交的是保存点之后的数据）
        transaction.savepoint_commit(sid)
        return redirect('/user/center_order/')
    except:
        # 回滚到保存点（所有要运行的操回滚到保存点）
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')


def pay(request,oid):
    order=OrderInfo.objects.get(pk=oid)
    order.oIsPay=True
    order.save()
    return redirect('/user/center_order/')
