import json

from django.http import JsonResponse

from apps.main.views import red
from util.token_auth import verify_auth_token


def authorization(func):  #自定义登录验证装饰器
    def wrapper(request,*args,**kwargs):
        request_data = json.loads(request.body)
        token = request_data.get('token', None)
        openid = request_data.get('openid', None)
        # 认证
        token_str = openid + str(red.hmget(openid,'postfix')[0],encoding='utf-8')
        if not verify_auth_token(token_str, token):
            return JsonResponse({'code': 400,'msg':'登陆过期，请重新登陆'})
        return func(request,*args,**kwargs)
    return wrapper