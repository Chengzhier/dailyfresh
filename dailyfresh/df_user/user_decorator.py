# coding=utf-8
from django.shortcuts import redirect
from django.http import JsonResponse


# 如果未登录则转到登陆页面
def login(func):
    print('111')
    def login_fun(request,*args,**kwargs):
        # print('222')
        if request.session.has_key('user_id'):
            # print '-------------------------'
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax:
                return JsonResponse({{'islogin':0}})
            else:
                return redirect('/user/login/')
            # red.set_cookie('url',request.get_full_path())
            # return red
    return login_fun
