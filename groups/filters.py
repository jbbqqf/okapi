# -*- coding: utf-8 -*-

from django_filters import FilterSet, CharFilter
from groups.models import Group

class GroupFilter(FilterSet):
    name = CharFilter(name='name', lookup_type='icontains')
    url = CharFilter(name='url', lookup_type='icontains')
    mailing = CharFilter(name='mailing', lookup_type='icontains')
    description = CharFilter(name='description', lookup_type='icontains')
    class Meta:
        model = Group
        fields = ['name', 'url', 'mailing', 'description', 'parent',]
