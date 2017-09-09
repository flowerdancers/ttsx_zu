#!/usr/bin/env python
#__*__coding:utf-8__*__
from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^login/$',views.login)
]


