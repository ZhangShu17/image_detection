# -*- coding: utf-8 -*-
from django.conf.urls import url
from direction import views
urlpatterns = [
	# post 请求控制方向盘
	url(r'^autodrive/direction/?$', views.CarMoveView.as_view(), name='direction'),
	# post 请求，运行状态转换 status=1 停车， status=0 开始行进
	url(r'^autodrive/change_status/?$', views.ChangeStopStatus.as_view(), name='change_status'),
	# get 请求获取当前指令, post请求将当前指令转换成已执行状态
	url(r'^autodrive/current_command/?$', views.CommandExecuView.as_view(), name='current_command'),
	# 手动自动切换指令
	url(r'^autodrive/control_state/?$', views.ControlStateView.as_view(), name='control_state'),
]