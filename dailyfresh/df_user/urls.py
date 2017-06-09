from django.conf.urls import url
import views

urlpatterns = [
    url('^$', views.index),
    url('^login/$', views.login),
    url('^register/$', views.register),
    url('^register_handle/$', views.register_handle),
    url('^register_exist/$', views.register_exist),
    url('^login_handle/$', views.login_handle),
    url('^logout/$',views.logout),
    url('^center_info/$', views.center_info),
    url('^center_order(\d*)/$', views.center_order),
    url('^center_site/$', views.center_site),


]
