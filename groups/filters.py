# -*- coding: utf-8 -*-

from django_filters import FilterSet, CharFilter, NumberFilter
from groups.models import Group

class GroupFilter(FilterSet):
    name = CharFilter(name='name', lookup_type='icontains',
                      label='name contain filter')
    url = CharFilter(name='url', lookup_type='icontains',
                     label='url contain filter')
    mailing = CharFilter(name='mailing', lookup_type='icontains',
                         label='mailing contain filter')
    description = CharFilter(name='description', lookup_type='icontains',
                             label='description contain filter')
    parent = NumberFilter(name='parent',
                          label='filter groups by their parent id')

    class Meta:
        model = Group
        fields = ['name', 'url', 'mailing', 'description', 'parent',]
