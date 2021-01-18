"""Movie_RS URL Configuration

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
from django.urls import path, re_path
from home import views

urlpatterns = [
    path('', views.Select.as_view(), name="select"),
    path('recommend/', views.RecommendForYou.as_view(), name="recommend"),
    path('douban_250/', views.Douban_250.as_view(), name="douban_250"),
    re_path('detail/(?P<imdbid>.*?)/', views.GetDetail.as_view(), name="detail"),
    path('search/', views.Search.as_view(), name="search"),
    path('browse_records/', views.BrowseRecords.as_view(), name="browse_records"),
]
