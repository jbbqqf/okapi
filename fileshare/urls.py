# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from fileshare.views import FileViewSet, DirectoryViewSet

router = DefaultRouter()
router.register(r'files', FileViewSet)
router.register(r'directories', DirectoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
