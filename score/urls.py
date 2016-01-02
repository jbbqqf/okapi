# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from score.views import ScoreView, CurrentScoreView

router = DefaultRouter()
router.register(r'scores', ScoreView)
router.register(r'currentscores', CurrentScoreView)

urlpatterns = [
    url(r'^', include(router.urls)),
]
