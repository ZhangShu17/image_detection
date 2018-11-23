# -*- coding: utf-8 -*-
from __future__ import division
from rest_framework import serializers
from monitor.models import PersonFace, CarDetection, Obstacle, Transaction


class TimeStampField(serializers.Field):
    def to_representation(self, value):
        try:
            time = str(value)
            time = time.split('.')[0]
        except Exception as e:
            print(Exception, ':', e)
            return "0"
        return time


class PersonFaceSerializer(serializers.ModelSerializer):
    create_at = TimeStampField()

    class Meta:
        model = PersonFace
        fields = (
            'id',
            'camera_id',
            'link_url',
            'create_at',
            'gender',
            'age',
            'longitude',
            'latitude',
            'loc_path',
            'uuid',
            'match_uuid'
        )


class CarDetectionSerializer(serializers.ModelSerializer):
    create_at = TimeStampField()

    class Meta:
        model = CarDetection
        fields = "__all__"


class ObstacleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obstacle
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    create_at = TimeStampField()
    trans_Obstacle = ObstacleSerializer(many=True)

    class Meta:
        model = Transaction
        fields = (
            'id',
            'car_id',
            'create_at',
            'longitude',
            'latitude',
            'velocity',
            'angle',
            'trans_Obstacle'
        )