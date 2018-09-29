#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file_name：'urls.py '
author：'baobinghuan'
create_time：'2018/9/27'
"""
from django.urls import path
from .import views

app_name = 'lists' # URL 名称添加命名空间,防止不同应用有重名url
urlpatterns = [
	path('', views.home_page, name='home_page'),
	
]