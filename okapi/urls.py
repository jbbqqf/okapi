"""okapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers
import users.views
import groups.views
import chat.views

router = routers.DefaultRouter()
router.register(r'users', users.views.UserViewSet)
router.register(r'profiles', users.views.ProfileViewSet)
router.register(r'groups', groups.views.GroupViewSet)
router.register(r'posts', chat.views.PostViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
]

# admin webinterface
urlpatterns += staticfiles_urlpatterns()
