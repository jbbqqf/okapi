# -*- coding: utf-8 -*-

from django.conf.urls import url
from grades.views import MyGradesView, MyJuriesView, MyCertificationsView

urlpatterns = [
    url(r'^mygrades/$', MyGradesView.as_view(), name='mygrades'),
    url(r'^myjuries/$', MyJuriesView.as_view(), name='myjuries'),
    url(r'^mycertifs/$', MyCertificationsView.as_view(), name='mycertifs'),
]
