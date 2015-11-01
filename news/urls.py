# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from rest_framework.routers import DefaultRouter
from news.views import EventView

router = DefaultRouter()
router.register(r'events', EventView)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
