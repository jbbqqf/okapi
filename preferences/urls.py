# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from preferences.views import UserInterfaceView, UserPrefView

router = DefaultRouter()
router.register(r'uis', UserInterfaceView, base_name='userinterfaces')
router.register(r'myprefs', UserPrefView, base_name='myprefs')

urlpatterns = [
    url(r'^', include(router.urls)),
]
