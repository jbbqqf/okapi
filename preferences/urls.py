from django.conf.urls import url, patterns, include

from rest_framework import routers

from preferences.views import UserInterfaceView, UserPrefView

router = routers.DefaultRouter()
router.register(r'uis', UserInterfaceView, base_name='userinterfaces')
router.register(r'mytheme', UserPrefView, base_name='mytheme')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
