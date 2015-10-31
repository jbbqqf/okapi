from django.conf.urls import url, patterns

from grades.views import MyGradesView

urlpatterns = patterns('',
    url(r'^mygrades/$', MyGradesView.as_view(), name='mygrades'),
)
