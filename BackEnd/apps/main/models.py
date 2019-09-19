import json
from datetime import datetime
from django_prometheus.models import ExportModelOperationsMixin

import bson
from django.db import models

# Create your models here.
from mongoengine import Document, StringField, IntField, ListField, EmbeddedDocumentField, BooleanField, ImageField, \
    URLField, EmbeddedDocument, ReferenceField,DateField,DateTimeField


class Settings(Document):
    pass


class Authorization(Document):
    pass


# waiting for edit
# 待加入限制最大activate Prize数为6
class Prize(Document):
    name = StringField(max_length=40, required=True)
    need_delivery = BooleanField()
    activate = BooleanField()
    stock = IntField()
    image_url = URLField()

    def to_json(self):
        return {
            "_id": str(self.pk),
            "name": self.name,
            "need_delivery": self.need_delivery,
            "activate": self.activate,
            "image_url": self.image_url
        }

    @property
    def id(self):
        return str(self.pk)


DELIVERY_STATE = (0, 1, 2, 3)
USER_PRIZE_STATE = (0,1,2,3)


class UserPrize(EmbeddedDocument):
    prize = ReferenceField(Prize)
    phone = IntField()
    state = IntField(choices=USER_PRIZE_STATE,default=0)
    delivery_state = IntField(choices=DELIVERY_STATE, default=0)
    created_time = DateTimeField()
    id = StringField(required=True,max_length=128,unique=True)





class RemainGame(EmbeddedDocument):
    is_daily_updated = BooleanField(default=False)
    normal = ListField(default=[10, 10])


class User(Document):
    openid = StringField(max_length=100, required=True, unique=True)
    nickname = StringField(max_length=100, required=True)
    phone = IntField()
    address = StringField(max_length=200)
    prizes = ListField(EmbeddedDocumentField(UserPrize))
    remain_game = EmbeddedDocumentField(RemainGame, default=RemainGame)
    remain_practice = IntField(default=3)
    points = IntField(default=0)
    score = IntField(default=0)
    invitation_code = StringField(max_length=100,required=True,unique=True)
    is_invited = BooleanField(default=False)
    inviter_openid = StringField(max_length=100)
    headimgurl = URLField()


    # #override
    # def to_json(self):
    #     return {
    #         "openid":self.openid,
    #         "nickname":self.nickname,
    #         "phone":self.phone,
    #         "address":self.address,
    #         "prizes":json.dumps([prize.to_json() for prize in self.prizes]),
    #         "remain_game":self.remain_game.to_json(),
    #         "remain_practice":self.remain_practice,
    #         "points":self.points,
    #         "score":self.score,
    #         "invitation_code":self.invitation_code,
    #         "headimgurl":self.headimgurl
    #     }


GARBAGE_TYPE = ('wet', 'dry', 'recyclable', 'harmful')


class Garbage(Document):
    name = StringField(max_length=100, required=True, unique=True)
    type = StringField(choices=GARBAGE_TYPE)
    image_url = URLField()



class RankingObject(EmbeddedDocument):
    openid = StringField(max_length=100, required=True, unique=True)
    score = IntField()


class WeekRanking(Document):
    activate = BooleanField()
    created_time = DateField()
    ranking_list = ListField(EmbeddedDocumentField(RankingObject))