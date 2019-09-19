import hashlib
import time

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from xml.dom.minidom import parse, parseString
import requests
import json

from apps.main.models import User
from apps.main.views import get_ticket, red
from util.common import rest_sec_of_day
from util.decorators import authorization
from util.token_auth import verify_auth_token
from util.wechat import Sign

access_token = "19_i3R89mNvWrvJY8a2VG3YD5Wlj-Fe_icL-MNykVOmt8SJpCVXF192z40In_bada3SOr9Zs3CV9Trx98CUs0W6XKZrJqwek1wvs1cQjGOnumfB8O8qAYrJMBv5yHYC8BEiRj6f9jxFZ7_YECNhAGUcAJAUAO"

app_id = 'wxa0c3aa5fdd1d1a78'
appsecret = 'a2210e72cefba5bc34b18850ab8024f3'
session_mock = {}


@csrf_exempt
def get_acess_token(request):
    if request.method == 'GET':
        # 从Session 获取
        user_tokens = session_mock.get('user_info', None)

        # Session没有则根据code来请求微信API
        if not user_tokens or not user_tokens.get('access_token',None):
            code = request.GET.get('code', None)
            if not code:
                return JsonResponse({'code': 400})

            url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(app_id, appsecret, code)
            user_tokens = json.loads(requests.get(url).content)
            print('user_tokens',user_tokens)
            # 设置 session
            if user_tokens.get('access_token'):
                session_mock['user_info'] = user_tokens

        # 获取用户数据
        user_info = get_user_infos(user_tokens.get('access_token'), user_tokens.get('open_id'))
        return JsonResponse({'code': 200, 'data': user_info}, json_dumps_params={'ensure_ascii': False})


# 获取用户 名头像等信息
def get_user_infos(access_token, open_id):
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN'.format(access_token, open_id)
    return json.loads(requests.get(url).content)


# def get_user_info(request):
#     user_info = session_mock.get('user_info',None)
#     if not user_info or  not user_info.get('access_token'):


@csrf_exempt
def regist_view(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        # 服务器配置中的token
        token = 'ktwechat'
        # 把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist]).encode('utf-8')
        hashstr = hashlib.sha1(hashstr).hexdigest()

        if hashstr == signature:
            return HttpResponse(echostr)
        else:

            return HttpResponse("field")

    if request.method == 'POST':
        root = parseString(request.body).documentElement
        caption_node = root.getElementsByTagName('Content')

        response_xml = '''
                    <xml>
                    <ToUserName><![CDATA[{}]]></ToUserName>
                    <FromUserName><![CDATA[{}]]></FromUserName>
                    <CreateTime>{}</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[{}]]></Content>
                    </xml>
        '''
        response = HttpResponse(
            response_xml.format('oY0r95yF4UPN6A3d7J7ddwmrHPVk', 'gh_6c7f0225c741', str(int(time.time())), 'hello'))
        response.content_type = 'application/xml'

        return response




@csrf_exempt
def get_jssdk_config(request):
    if request.method == 'POST':
        ticket = get_ticket()
        url = json.loads(request.body).get('url',None)
        if not ticket or not url:
            return HttpResponseServerError
        sign = Sign(ticket, url)
        config = sign.sign()
        config['appid'] = app_id
        return JsonResponse({'code': 200, 'data': config})



# @csrf_exempt
# def wx_share(request):
#     if request.method == 'POST':
#         request_data = json.loads(request.body)
#         token = request_data.get('token', None)
#         openid = request_data.get('openid', None)
#         type = request_data.get('type', None) # timeline: 朋友圈; friend: 好友
#
#
#         # 认证
#         token_str = openid + str(red.hmget(openid,'postfix')[0],encoding='utf-8')
#         if verify_auth_token(token_str, token):
#             return JsonResponse({'code': 400,'msg':'登陆过期，请重新登陆'})
#
#         if not type:
#             return JsonResponse({'code': 400,'msg':'参数错误'})
#
#         user = User.objects.get(openid=openid)
#         key = "{}Share:{}".format(type,openid)
#         user_share = red.get(key)
#
#         if not user_share:
#             expire = rest_sec_of_day()
#             red.setex(key,expire,0)
#             user_share = 0
#
#         if int(user_share) >= share_count[type]['count']:
#             return JsonResponse({'code': 400, 'data': '','msg':share_count[type]['msg']})
#
#         user.remain_game.normal = [user.remain_game.normal[0] + 1, user.remain_game.normal[1]]
#         red.incr(key)
#         user.save()
#
#
#         return JsonResponse({'code': 200, 'data': '','msg':'分享成功，您的游戏次数增加一次'})
#

@csrf_exempt
@authorization
def wx_share(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        openid = request_data.get('openid', None)
        type = request_data.get('type', None) # timeline: 朋友圈; friend: 好友


        if not type:
            return JsonResponse({'code': 400,'msg':'参数错误'})

        user = User.objects.get(openid=openid)
        key = "{}Share:{}".format(type,openid)
        user_share = red.get(key)

        if not user_share:
            expire = rest_sec_of_day()
            red.setex(key,expire,0)
            user_share = 0

        if int(user_share) >= share_count[type]['count']:
            return JsonResponse({'code': 400, 'data': '','msg':share_count[type]['msg']})

        user.remain_game.normal = [user.remain_game.normal[0] + 1, user.remain_game.normal[1]]
        red.incr(key)
        user.save()


        return JsonResponse({'code': 200, 'data': '','msg':'分享成功，您的游戏次数增加一次'})


share_count = {
    'timeline':{
        'count':1,
        'msg':'您的今日朋友圈分享次数已完成'
    },
    'friend':{
        'count':5,
        'msg':'您的今日好友分享已全部完成'
    }
}
def test(request):
    if request.method == 'GET':

        openid = "oY0r95yF4UPN6A3d7J7ddwmrHPVk"
        user = User.objects.get(openid=openid)
        type = "timeline"
        user_share = 'what'
        key = "{}Share:{}".format(type,openid)
        print('key',key)
        user_share = red.get(key)

        if not user_share:
            expire = rest_sec_of_day()
            red.setex(key,expire,0)
            print("here")
            user_share = 0

        print('user_share',user_share)
        if int(user_share) >= share_count[type]['count']:
            return JsonResponse({'code': 400, 'data': '','msg':share_count[type]['msg']})

        user.remain_game.normal = [user.remain_game.normal[0] + 1, user.remain_game.normal[1]]
        red.incr(key)
        user.save()

        return JsonResponse({'code': 200, 'data': '','msg':'分享成功，您的游戏次数增加一次'})


