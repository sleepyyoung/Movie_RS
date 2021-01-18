"""WBHotSearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path, re_path, include, reverse
from django.views import View
from django.contrib import auth  # 引入auth模块
from django.contrib.auth.models import User  # auth应用中引入User类
from enter import views

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('register/', views.Register.as_view(), name="register"),
    path('logout/', views.Logout.as_view(), name="logout"),
    re_path('modify/(?P<method>.*?)/(?P<username>.*?)/', views.Modify.as_view(), name="modify"),
    re_path('forgot_password/(?P<username>.*?)/', views.ForgotPassword.as_view(), name="forgot_password"),
    path('send_email/', views.SendEmail.as_view(), name="send_email")
]
