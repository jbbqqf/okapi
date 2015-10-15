from django.conf.urls import url, patterns, include

from rest_framework import routers

from profiles.views import ProfileViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = patterns('',
    url(r'^users/', include(router.urls)),
)
