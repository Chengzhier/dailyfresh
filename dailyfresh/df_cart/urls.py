# coding=utf-8
from django.conf.urls import url
import views


urlpatterns=[
    url('^$', views.carts),
    # 那个商品，多少个
    url('^add(\d+)_(\d+)/$', views.add),
    url('^count_change/$',views.count_change),
    url('^delete/$',views.delete),
    url('^order/$',views.order),
]
