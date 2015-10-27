from django.conf.urls import url, patterns, include
from rest_framework import routers
from news.views import EventView

router = routers.DefaultRouter()
router.register(r'events', EventView)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
