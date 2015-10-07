from django.conf.urls import url, patterns

from okauth.views import LoginView, LogoutView

urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
)
