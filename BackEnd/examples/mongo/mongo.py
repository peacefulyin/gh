import json

from bson import json_util
from django.db import models

# Create your models here.
from django.http import JsonResponse
from mongoengine import Document, StringField, IntField, ListField, EmbeddedDocumentField, BooleanField, ImageField, \
    URLField, EmbeddedDocument, connect,ReferenceField
from apps.main.models import Prize

from apps.main.models import Prize,User,UserPrize,RemainGame,Garbage
connect("garbage_hero",host="192.168.40.130",port=27018)
#
# from django.conf import settings
# settings.configure()


def create_prize():
    prize_name_list = [
        {
            "name": "卡通车",
            "url": "http://172.10.3.98:8001/static/gift_car.png"
        },
        {
            "name": "手提包",
            "url": "http://172.10.3.98:8001/static/gift_pag.png"
        },
        {
            "name": "保温杯",
            "url": "http://172.10.3.98:8001/static/gift_thermos.png"
        },
        {
            "name": "垃圾桶",
            "url": "http://172.10.3.98:8001/static/gift_barrel.png"
        },
        {
            "name": "10积分",
            "url": "http://172.10.3.98:8001/static/20.png"
        },
        {
            "name": "50积分",
            "url": "http://172.10.3.98:8001/static/20.png"
        }
    ]
    for index,item in enumerate(prize_name_list):
        activate = True
        if index>=5:
            activate = False
        print('index',index)
        prize = Prize.objects.create(name=item['name'],activate=activate,image_url=item['url'])

        prize.save()


create_prize()

