from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^home/', 'demo.views.home'),
    url(r'^error/', 'demo.views.error'),
    url(r'^bugs/', 'demo.views.bugs'),
    url(r'^login/', 'demo.views.login'),
    url(r'^api_login/', 'demo.views.api_login'),
    url(r'^sign/', 'demo.views.sign'),
    url(r'^api_sign/', 'demo.views.api_sign'),
    # url(r'^index/', 'demo.views.index'),
    url(r'^weather/', 'demo.views.weather'),
]