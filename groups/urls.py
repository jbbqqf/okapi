# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from rest_framework.routers import DefaultRouter
from groups.views import GroupViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
