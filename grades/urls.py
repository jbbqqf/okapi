# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from grades.views import MyGradesView, MyJuriesView

urlpatterns = patterns(
    '',
    url(r'^mygrades/$', MyGradesView.as_view(), name='mygrades'),
    url(r'^myjuries/$', MyJuriesView.as_view(), name='myjuries'),
)
