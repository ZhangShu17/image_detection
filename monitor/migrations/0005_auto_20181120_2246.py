# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-20 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20181116_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardetection',
            name='loc_path',
            field=models.CharField(max_length=100, null=True, verbose_name='\u672c\u5730\u6587\u4ef6\u5730\u5740'),
        ),
        migrations.AddField(
            model_name='personface',
            name='loc_path',
            field=models.CharField(max_length=100, null=True, verbose_name='\u672c\u5730\u6587\u4ef6\u5730\u5740'),
        ),
    ]
