# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from online.views import PresenceView

router = DefaultRouter()
router.register(r'presence', PresenceView, base_name='presence')

urlpatterns = [
    url(r'^', include(router.urls)),
]
