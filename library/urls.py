# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from library.views import PressReviewView

router = DefaultRouter()
router.register(r'pressreviews', PressReviewView)

urlpatterns = [
    url(r'^', include(router.urls)),
]
