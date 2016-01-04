# -*- coding: utf-8 -*-

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
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^okauth/', include('okauth.urls')),
    url(r'^users/', include('profiles.urls')),
    url(r'^users/', include('groups.urls')),
    url(r'^users/', include('online.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^share/', include('fileshare.urls')),
    url(r'^prefs/', include('preferences.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^grades/', include('grades.urls')),
    url(r'^library/', include('library.urls')),
    url(r'^score/', include('score.urls')),
    url(r'^button/', include('button.urls')),

    url(r'^{}/(.*)$'.format(settings.PRIVATE_MEDIA_URL),
        'common.private_media.serve_private_media'),

    url(r'^docs/', include('rest_framework_swagger.urls')),
]

if settings.DEBUG:
    # admin webinterface
    urlpatterns += staticfiles_urlpatterns()

    # serving media files
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
