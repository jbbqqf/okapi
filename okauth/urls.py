# -*- coding: utf-8 -*-

from django.conf.urls import url
from okauth.views import LoginView, LogoutView, CheckTokenView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^checktoken/$', CheckTokenView.as_view(), name='checktoken'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]
