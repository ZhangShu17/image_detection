# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# 负责人
class PersonInCharge(models.Model):
    name = models.CharField(max_length=10, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'电话')

    class Meta:
        unique_together = (('name', 'mobile'),)


# 车辆信息
class Car(models.Model):
    car_sign = models.CharField(max_length=20, verbose_name=u'车牌')
    in_charge = models.ManyToManyField(to=PersonInCharge, related_name='person_car')
    car_type = models.CharField(max_length=10, null=True, verbose_name='车型')

    class Meta:
        unique_together = (('car_sign', 'car_type'),)


# 相机
class Camera(models.Model):
    camera_sign = models.CharField(max_length=20, verbose_name=u'相机编号')
    car = models.ForeignKey(to=Car, related_name='car_camera', on_delete=models.CASCADE,verbose_name=u'所属车辆')

    class Meta:
        unique_together = (('camera_sign', 'car'),)


# 车辆运行轨迹
class Transaction(models.Model):
    car = models.ForeignKey(to=Car, related_name='car_trans', on_delete=models.CASCADE, verbose_name=u'所属车辆')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    longitude = models.CharField(max_length=15, verbose_name=u'经度')
    latitude = models.CharField(max_length=15, verbose_name=u'纬度')
    velocity = models.FloatField(max_length=5, null=True, verbose_name=u'速度')
    angle = models.FloatField(max_length=5, null=True, verbose_name=u'方向')

    class Meta:
        unique_together = (('car', 'create_at'),)


# 障碍物记录
class Obstacle(models.Model):
    length = models.FloatField(max_length=5, null=True, verbose_name=u'长度')
    width = models.FloatField(max_length=5, null=True, verbose_name=u'宽度')
    height = models.FloatField(max_length=5, null=True, verbose_name=u'高度')
    distance = models.FloatField(max_length=5, null=True, verbose_name=u'距离')
    angle = models.FloatField(max_length=5, null=True, verbose_name=u'角度')
    transaction = models.ForeignKey(to=Transaction, on_delete=models.CASCADE, related_name='trans_Obstacle')


# 人脸图片
class PersonFace(models.Model):
    camera = models.ForeignKey(to=Camera, on_delete=models.CASCADE, related_name=u'camera_person_face')
    link_url = models.CharField(max_length=100, verbose_name=u'链接地址')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    gender = models.CharField(max_length=1, null=True, verbose_name=u'性别')
    age = models.CharField(max_length=5, null=True, verbose_name=u'年龄')
    longitude = models.CharField(max_length=15, null=True, verbose_name=u'经度')
    latitude = models.CharField(max_length=15, null=True, verbose_name=u'纬度')
    loc_path = models.CharField(max_length=100, null=True, verbose_name=u'本地文件地址')
    uuid = models.CharField(max_length=100, null=True)
    match_uuid = models.CharField(max_length=100, null=True)


# 车辆图片
class CarDetection(models.Model):
    camera = models.ForeignKey(to=Camera, on_delete=models.CASCADE, related_name=u'camera_car_detec')
    link_url = models.CharField(max_length=100, verbose_name=u'链接地址')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    length = models.FloatField(max_length=5, null=True, verbose_name=u'长度')
    width = models.FloatField(max_length=5, null=True, verbose_name=u'宽度')
    height = models.FloatField(max_length=5, null=True, verbose_name=u'高度')
    plate_num = models.CharField(max_length=10, null=True, verbose_name=u'车牌号')
    longitude = models.CharField(max_length=15, null=True, verbose_name=u'经度')
    latitude = models.CharField(max_length=15, null=True, verbose_name=u'纬度')
    loc_path = models.CharField(max_length=100, null=True, verbose_name=u'本地文件地址')
    uuid = models.CharField(max_length=100, null=True)
    match_uuid = models.CharField(max_length=100, null=True)