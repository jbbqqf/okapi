# -*- coding: utf-8 -*-

from django_filters import FilterSet, CharFilter, DateTimeFilter
from chat.models import Post

class PostFilter(FilterSet):
    datefrom = DateTimeFilter(name='date', lookup_type='gte')
    dateto = DateTimeFilter(name='date', lookup_type='lte')
    content = CharFilter(name='content', lookup_type='icontains')
    class Meta:
        model = Post
        fields = ['author', 'type', 'content', 'datefrom', 'dateto',]
