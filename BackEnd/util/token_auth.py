from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from django.conf import settings

def generate_auth_token(key, expiration=36000):
    s = Serializer(settings.SECRET_KEY, expires_in=expiration)
    return s.dumps({'key': key})


def verify_auth_token(key, token):
    s = Serializer(settings.SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return 0  # valid token, but expired
    except BadSignature:
        return -1  # invalid token
    return data['key'] == key



