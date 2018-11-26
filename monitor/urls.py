# -*- coding: utf-8 -*-
from django.conf.urls import url
from monitor import views

urlpatterns = [
    url(r'^face_detection/?', views.FaceDetectionView.as_view()),
    url(r'^transaction/?', views.TransactionView.as_view()),
	url(r'^obstacle/?', views.ObstacleView.as_view()),
]