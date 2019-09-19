from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'regist', views.regist_view),
    re_path(r'get_acess_token', views.get_acess_token),
    re_path(r'get_jssdk_config$', views.get_jssdk_config),
    re_path(r'wx_share', views.wx_share),


]