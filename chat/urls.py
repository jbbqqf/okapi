from django.conf.urls import url, patterns, include

from rest_framework import routers

from chat.views import PostViewSet, ChannelView

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'channels', ChannelView, base_name='channels')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
