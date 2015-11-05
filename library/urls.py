# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from rest_framework.routers import DefaultRouter
from library.views import PressReviewView

router = DefaultRouter()
router.register(r'pressreviews', PressReviewView)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
