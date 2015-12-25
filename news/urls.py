# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from news.views import EventView

router = DefaultRouter()
router.register(r'events', EventView)

urlpatterns = [
    url(r'^', include(router.urls)),
]
