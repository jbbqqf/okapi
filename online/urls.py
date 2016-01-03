# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from online.views import active, passive, away, toggle_away, PresenceView

router = DefaultRouter()
router.register(r'presence', PresenceView, base_name='presence')

urlpatterns = [
    url(r'^presence/active/$', active),
    url(r'^presence/passive/$', passive),
    url(r'^presence/away/$', away),
    url(r'^presence/toggle_away/$', toggle_away),
    url(r'^', include(router.urls)),
]
