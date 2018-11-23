# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class MonitorConfig(AppConfig):
    name = 'monitor'

    def ready(self):
        import signals.handler1
