from django.conf.urls import url, patterns, include

from rest_framework import routers

from fileshare.views import FileViewSet, DirectoryViewSet

router = routers.DefaultRouter()
router.register(r'files', FileViewSet)
router.register(r'directories', DirectoryViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
