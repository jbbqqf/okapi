# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from rest_framework.routers import DefaultRouter
from chat.views import PostViewSet, ChannelView

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'channels', ChannelView, base_name='channels')

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
