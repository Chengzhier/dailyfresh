# coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from df_cart.models import *
# Create your views here.

def index(request):
    typelist=TypeInfo.objects.all()
    list=[]
    for type in typelist:
        list.append({
            'type':type,
            'click_list':type.goodsinfo_set.order_by('-gclick')[0:3],
            'new_list':type.goodsinfo_set.order_by('-id')[0:4]
        })
        context={'title':'首页',
                 'list':list,'cart_count':cart_count(request)}
    return render(request,'df_goods/index.html',context)



def list(request,tid,pindex,orderby):
    gtype=TypeInfo.objects.get(id=int(tid))
    new_list=gtype.goodsinfo_set.order_by('-id')[0:2]
    # 查询指定分类tid的商品
    goods_list = GoodsInfo.objects.filter(gtype_id=int(tid))
    if orderby == "1":
        goods_list = goods_list.order_by('-id')
    elif orderby == "2":
        goods_list = goods_list.order_by('-gprice')
    elif orderby =="3":
        goods_list = goods_list.order_by('-gclick')

    #分页
    paginator=Paginator(goods_list,10)
    pindex2 = int(pindex)
    if pindex2<= 0:
        pindex2=1
    elif pindex2 >paginator.num_pages:
        pindex2 = paginator.num_pages
    page=paginator.page(pindex2)
    context={'title':'列表页','page':page,'tid':tid,'gtype':gtype,'orderby':orderby,'new_list':new_list,'cart_count':cart_count(request)}
    return render(request,'df_goods/list.html',context)


def detail(request,gid):
    goods = GoodsInfo.objects.get(pk=gid)
    goods.gclick = goods.gclick+1
    goods.save()
    new_list=goods.gtype.goodsinfo_set.order_by('-id')[0:2]

    context={'title':'商品详细','goods':goods,'new_list':new_list,'cart_count':cart_count(request)}
    response=render(request,'df_goods/detail.html',context)
    # 最近浏览
    liulan=request.COOKIES.get('liulan','')
    if liulan=='':
        response.set_cookie('liulan',gid)
    else:
        liulan_list=liulan.split(',')
        if gid in liulan_list:
            liulan_list.remove(gid)
        liulan_list.insert(0,gid)
        if len(liulan_list)>5:
            liulan_list.pop()
        liulan2=','.join(liulan_list)
        response.set_cookie('liulan',liulan2)
    return response

# def search(request):
#     return render(request,'search/search.html')
from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        extra = super(MySearchView, self).extra_context()
        extra['title']=self.request.GET.get('q')
        return extra


def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0