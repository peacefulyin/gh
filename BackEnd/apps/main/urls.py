from django.urls import re_path

from . import views


urlpatterns = [
    # re_path(r'mongocreate$', views.mongocreate),
    re_path(r'ranking$', views.ranking),
    re_path(r'get_user_info$', views.get_user_info),
    re_path(r'play$', views.play),
    re_path(r'finish_game$', views.finish_game),
    re_path(r'start_lottery$', views.start_lottery),
    re_path(r'get_prizes$', views.get_prizes),
    re_path(r'test_prizes', views.test_prizes),
    re_path(r'get_user_prizes$', views.get_user_prizes),
    re_path(r'invitation$', views.invitation),
    re_path(r'get_access_token$', views.get_access_token),
    re_path(r'get_ticket$', views.get_ticket),
    # re_path(r'get_jssdk_config$', views.get_jssdk_config),
    # re_path(r'heart_beat$', views.heart_beat),
    # re_path(r'task', views.task),
]