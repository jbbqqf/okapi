# -*- coding: utf-8 -*-

from django_filters import FilterSet, CharFilter, DateTimeFilter
from chat.models import Post

class PostFilter(FilterSet):
    author = CharFilter(name='author', lookup_type='icontains',
                        label='author contain filter')
    type = CharFilter(name='type', label='filter on letter value')
    content = CharFilter(name='type', lookup_type='icontains',
                         label='content contain filter')
    dflabel = 'filter posts posted after or on provided date / time'
    datefrom = DateTimeFilter(name='date', lookup_type='gte', label=dflabel)
    dtlabel = 'filter posts posted before or on provided date / time'
    dateto = DateTimeFilter(name='date', lookup_type='lte', label=dtlabel)
    content = CharFilter(name='content', lookup_type='icontains',
                         label='content contain filter')

    class Meta:
        model = Post
        fields = ['author', 'type', 'content', 'datefrom', 'dateto',]
