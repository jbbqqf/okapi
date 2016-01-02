# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from button.views import clear, ClearView

router = DefaultRouter()
router.register(r'clears', ClearView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^clear/$', clear)
]
