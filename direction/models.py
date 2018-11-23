# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mongoengine


# Create your models here.
class Command(mongoengine.Document):
    time = mongoengine.IntField()
    execute = mongoengine.BooleanField(default=False)
    angle = mongoengine.IntField(min_value=-360, max_value=360)
    total_angle = mongoengine.IntField()


class StopStatus(mongoengine.Document):
    stop_status = mongoengine.BooleanField(default=False)


class ControlState(mongoengine.Document):
    control_status = mongoengine.BooleanField(default=True)

