# -*- coding: utf-8 -*-

from django_filters import FilterSet, CharFilter, DateTimeFilter, NumberFilter
from fileshare.models import File, Directory

class FileFilter(FilterSet):
    name = CharFilter(name='name', lookup_type='icontains',
                      label='name contain filter')
    parent = NumberFilter(name='parent', label='parent dir id filter')
    creator = NumberFilter(name='creator', label='user id filter')

    cafterlabel = 'filter files uploaded after or on provided date/time'
    created_after = DateTimeFilter(name='created', lookup_type='gte',
                                   label=cafterlabel)
    cbeforelabel = 'filter files uploaded before or on provided date/time'
    created_before = DateTimeFilter(name='created', lookup_type='lte',
                                    label=cbeforelabel)

    mafterlabel = 'filter files modified after or on provided date/time'
    modified_after = DateTimeFilter(name='modified', lookup_type='gte',
                                    label=mafterlabel)
    mbeforelabel = 'filter files modified before or on provided date/time'
    modified_before = DateTimeFilter(name='modified', lookup_type='lte',
                                     label=mbeforelabel)

    class Meta:
        model = File
        fields = ['name', 'parent', 'creator', 'created_after',
                  'created_before', 'modified_after', 'modified_before',]

class DirectoryFilter(FilterSet):
    name = CharFilter(name='name', lookup_type='icontains',
                      label='name contain filter')
    parent = NumberFilter(name='parent', label='parent dir id filter')

    cafterlabel = 'filter dirs uploaded after or on provided date/time'
    created_after = DateTimeFilter(name='created', lookup_type='gte',
                                   label=cafterlabel)
    cbeforelabel = 'filter dirs uploaded before or on provided date/time'
    created_before = DateTimeFilter(name='created', lookup_type='lte',
                                    label=cbeforelabel)

    mafterlabel = 'filter dirs modified after or on provided date/time'
    modified_after = DateTimeFilter(name='modified', lookup_type='gte',
                                    label=mafterlabel)
    mbeforelabel = 'filter dirs modified before or on provided date/time'
    modified_before = DateTimeFilter(name='modified', lookup_type='lte',
                                     label=mbeforelabel)

    class Meta:
        model = Directory
        fields = ['name', 'parent', 'created_after', 'created_before',
                  'modified_after', 'modified_before',]
