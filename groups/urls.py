# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from groups.views import GroupViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
