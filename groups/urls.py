from django.conf.urls import url, patterns, include

from rest_framework import routers

from groups.views import GroupViewSet

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
