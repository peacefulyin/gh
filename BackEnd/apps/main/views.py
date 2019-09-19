import datetime
import json
import random
import uuid

import redis
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from util.token_auth import generate_auth_token, verify_auth_token
from .models import User, Prize, UserPrize

# redis 初始化
pool = redis.ConnectionPool(host='192.168.40.130', password='qweqwe123', port=6379, db=1)
red = redis.Redis(connection_pool=pool)

app_id = 'wxa0c3aa5fdd1d1a78'
appsecret = 'a2210e72cefba5bc34b18850ab8024f3'


# #排行版Redis实现
# class RankingView(View):
#     def get(self, request):
#         total = request.GET.get('total', None)
#         if not total:
#             return JsonResponse({'code': 400})
#         ranking_list = red.zrevrange("rank_set", 0, total, withscores=True)
#         result = [[str(item[0], encoding="utf-8"), item[1]] for item in ranking_list]
#         return JsonResponse({'code': 200, "data": result})


# 排行版 MongoDB实现
# type 1: 周榜  2: 总榜

@csrf_exempt
def ranking(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        token = request_data.get('token', None)
        openid = request_data.get('openid', None)
        ranking_type = request_data.get('type', None)

        token_str = openid + str(red.hmget(openid, 'postfix')[0], encoding='utf-8')

        if not ranking_type or not verify_auth_token(token_str, token) or ranking_type not in [1, 2]:
            return JsonResponse({'code': 400})

        if ranking_type == 1:
            return

        if ranking_type == 2:
            users = User.objects.order_by('-score').limit(20)
            return JsonResponse({'code': 200, 'data': {'ranking_list': users.to_json()}})


class RankingView(View):
    def get(self, request):
        type = request.method
        total = request.GET.get('total', None)
        if not total:
            return JsonResponse({'code': 400})
        ranking_list = red.zrevrange("rank_set", 0, total, withscores=True)
        result = [[str(item[0], encoding="utf-8"), item[1]] for item in ranking_list]
        return JsonResponse({'code': 200, "data": result})


def get_access_token():
    access_token = red.get('wx:ticket')
    if not access_token:
        token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(
            app_id, appsecret)  # 创建获取token的url
        token_obj = requests.get(token_url).json()
        print(token_obj)
        access_token = token_obj.get("access_token")
        print('access_token', access_token)
        red.setex('wx:access_token', 7200, access_token)
        print("here")
    return access_token


def get_ticket():
    ticket = None
    try:
        ticket = str(red.get('wx:ticket'), encoding='utf-8')
    except Exception as e:
        print(e)
    if not ticket:
        access_token = get_access_token()
        ticket_url = " https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi".format(
            access_token)
        ticket_obj = requests.get(ticket_url).json()
        ticket = ticket_obj.get('ticket')
        red.setex('wx:ticket', 7200, ticket)
    return ticket


def refresh_access_token():
    pass


def get_user_info(request):
    if request.method == 'GET':
        # 从Session 获取
        # Session没有则根据code来请求微信API
        code = request.GET.get('code', None)

        before_invitation_code = int(red.get('invitation_code'))
        print('1')
        if not code:
            return JsonResponse({'code': 400})
        print('2')
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(
            app_id, appsecret, code)
        user_tokens = json.loads(requests.get(url).content)
        access_token = user_tokens.get('access_token')

        api_open_id = user_tokens.get('open_id')
        print("accesstoken", access_token)

        # 获取用户数据
        user_info = user_infos_api(access_token, api_open_id)
        print('user_info', user_info)
        print('3')
        open_id = user_info.get('openid', False)
        if not open_id:
            return JsonResponse({'code': 400})

        # 根据openid生成token
        postfix = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
        red.hmset(open_id, {'postfix': postfix})
        token_str = open_id + postfix
        token = generate_auth_token(token_str)
        print('token', token)
        try:
            user = User.objects.get(openid=user_info['openid'])
        except Exception as e:
            user = User.objects.create(openid=user_info['openid'], nickname=user_info['nickname'],
                                       invitation_code=str(before_invitation_code + 1))

        user.headimgurl = user_info['headimgurl']

        user.save()
        print('7')
        red.incr('invitation_code')
        user_data = user._data

        del user_data['id']
        return JsonResponse({"code": 200, "data": user.to_json(), 'token': str(token, encoding='utf-8')},
                            json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def play(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        token = request_data.get('token', None)
        openid = request_data.get('openid', None)
        type = request_data.get('type', None)

        token_str = openid + str(red.hmget(openid, 'postfix')[0], encoding='utf-8')

        if not token or not verify_auth_token(token_str, token):
            return JsonResponse({'code': 400})
        user = User.objects.get(openid=openid)
        if type == "normal":
            normal_game_count = user.remain_game.normal
            if normal_game_count[0] < 1:
                return JsonResponse({'code': 400})
            normal_game_count_after = [normal_game_count[0] - 1, normal_game_count[1]]
            user.remain_game.normal = normal_game_count_after
            user.save()
            return JsonResponse({'code': 200, 'remain_game': normal_game_count_after})


@csrf_exempt
def finish_game(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        token = request_data.get('token', None)
        openid = request_data.get('openid', None)
        score = request_data.get('score', None)

        token_str = openid + str(red.hmget(openid, 'postfix')[0], encoding='utf-8')

        if not token or not verify_auth_token(token_str, token):
            return JsonResponse({'code': 400})
        user = User.objects.get(openid=openid)
        if score >= 7:
            user.points += 10
        user.score += score
        user.save()
        return JsonResponse({'code': 200, 'data': {'score': user.score, 'points': user.points}})


# 获取用户 名头像等信息
def user_infos_api(access_token, open_id):
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN'.format(access_token, open_id)
    return json.loads(requests.get(url).content)


class UserView():
    def get(self, request):
        pass

    def post(self, request):
        pass


def login(request):
    openid = request.GET.get('openid', None)
    if not openid:
        return JsonResponse({'code': 400})
    token = generate_auth_token(openid)
    return JsonResponse({'code': 200, "token": token})


class ScoreView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


@csrf_exempt
def get_prizes(requests):
    if requests.method == 'POST':
        activate_prizes = Prize.objects.filter(activate=True)[:5]
        activate_prizes = json.dumps([prize.to_json() for prize in activate_prizes])
        return JsonResponse({'code': 200, 'data': activate_prizes})


def test_prizes(requests):
    if requests.method == 'GET':
        activate_prizes = Prize.objects.filter(activate=True)[:5]
        activate_prizes = json.dumps([prize.to_json() for prize in activate_prizes])
        return JsonResponse({'code': 200, 'data': activate_prizes})


@csrf_exempt
def get_user_prizes(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        openid = request_data.get('openid', None)
        token = request_data.get('token', None)

        token_str = openid + str(red.hmget(openid, 'postfix')[0], encoding='utf-8')

        if not (verify_auth_token(token_str, token)):
            return JsonResponse({'code': 400})
        user = User.objects.get(openid=openid)
        ret_list = []
        for user_prize in user.prizes:
            user_prize.created_time = user_prize.created_time -datetime.timedelta(hours=8)
            temp = user_prize.prize.to_json()
            user_prize = json.loads(user_prize.to_json())
            user_prize['prize'] = temp

            # ret_list.append(json.dumps(user_prize))
            ret_list.append(user_prize)
        print("ret_list",ret_list)
        # user_prizes = json.dumps([prize.to_json() for prize in user.prizes])
        # user_prizes = json.dumps(ret_list)
        user_prizes = ret_list

        return JsonResponse({'code': 200, 'data': {'user_prizes': user_prizes}})


@csrf_exempt
def start_lottery(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        openid = request_data.get('openid', None)
        token = request_data.get('token', None)
        print("datetime.datetime.now()",datetime.datetime.now())
        print("datetime.datetime.now()",datetime.datetime.now())
        # type = request_data.get('type',None) 后期可加入type
        # 认证

        token_str = openid + str(red.hmget(openid, 'postfix')[0], encoding='utf-8')

        if not (verify_auth_token(token_str, token)):
            return JsonResponse({'code': 400})
        user = User.objects.get(openid=openid)
        if user.points < 10:
            return JsonResponse({'code': 400, 'msg': '积分不够'})
        user.points -= 10
        prize_index = random.randint(0, 5)  # 0-5
        if prize_index == 5:
            return JsonResponse({'code': 200, 'data': {'prize_id': None}})
        activate_prizes = Prize.objects.filter(activate=True)

        prize_obj = activate_prizes[prize_index]
        user_prize = UserPrize(prize=prize_obj,id=str(uuid.uuid4()),created_time = datetime.datetime.now())
        if "积分" in prize_obj.name:
            print("积分加了")
            user.points += int(prize_obj.name[:2])
            user_prize.delivery_state = 3
        print("user_prize create time ",user_prize.created_time)

        user.prizes.append(user_prize)
        user.save()
        return JsonResponse({'code': 200, 'data': {'prize_id': str(prize_obj.id)}})


# def mongocreate(request):
#     user1 = User.objects.create(openid="1", name="1")
#     print('user1', user1)
#     return HttpResponse("ok")

@csrf_exempt
def invitation(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        token = request_data.get('token', None)
        openid = request_data.get('openid', None)
        invitation_code = request_data.get('invitationCode', None)
        # type = request_data.get('type',None) 后期可加入type
        # 认证

        token_str = openid + str(red.hmget(openid, 'postfix')[0], encoding='utf-8')

        if not invitation_code or not (verify_auth_token(token_str, token)):
            return JsonResponse({'code': 400})

        invitee = User.objects.get(openid=openid)
        if invitee.is_invited:
            return JsonResponse({'code': 400, 'msg': '您已经使用过邀请码。'})

        try:
            inviter = User.objects.get(invitation_code=invitation_code)
            if inviter.openid == openid:
                return JsonResponse({'code': 400, 'msg': '不能邀请你自己。'})
        except:
            return JsonResponse({'code': 400, 'msg': '邀请码无效。'})

        print('4')

        invitee.remain_game.normal = [invitee.remain_game.normal[0] + 1, invitee.remain_game.normal[1]]
        inviter.remain_game.normal = [inviter.remain_game.normal[0] + 1, inviter.remain_game.normal[1]]
        invitee.is_invited = True
        invitee.save()
        inviter.save()
        return JsonResponse({'code': 200, 'data': {'points': invitee.points}, 'msg': '成功使用邀请码，您和您的朋友均获得增加一次游戏机会。'})


change_type = ('remain_game', 'points', 'score')


# def heart_beat(request):
#     request_data = json.loads(request.body)
#     token = request_data.get('token', None)
#     openid = request_data.get('openid', None)
#     invitation_code = request_data.get('invitationCode', None)
#     # type = request_data.get('type',None) 后期可加入type
#     print('1')
#     # 认证
#     if not invitation_code or not (verify_auth_token(openid, token)):
#         return JsonResponse({'code': 400})
#     user = User.objects.get(openid=openid)


def dailyRefresh():
    User.objects().update(set__remain_game__normal=[5, 5])

# def task(request):
#     create_prize()
#     return JsonResponse({"code": 200})
