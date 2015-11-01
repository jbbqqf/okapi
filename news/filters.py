# -*- coding: utf-8 -*-

from django_filters import FilterSet, CharFilter, NumberFilter, DateTimeFilter
from news.models import Event


class EventFilter(FilterSet):
    author = NumberFilter(name='author', label='filter by author id')
    title = CharFilter(name='title', lookup_type='icontains',
                       label='title contain filter')
    description = CharFilter(name='description', lookup_type='icontains',
                             label='description contain filter')
    link = CharFilter(name='link', lookup_type='icontains',
                      label='link contain filter')

    ca_label = 'filter events created after or on provided date / time'
    created_after = DateTimeFilter(name='created', lookup_type='gte',
                                   label=ca_label)
    cb_label = 'filter events created after or on provided date / time'
    created_before = DateTimeFilter(name='created', lookup_type='lte',
                                    label=cb_label)

    da_label = 'filter events happening after or on provided date'
    dday_after = DateTimeFilter(name='dday', lookup_type='gte',
                                label=da_label)
    db_label = 'filter events happening before or on provided date'
    dday_before = DateTimeFilter(name='dday', lookup_type='lte',
                                 label=db_label)
    do_label = 'filter events happening on provided date'
    dday_on = DateTimeFilter(name='dday', label=do_label)

    class Meta:
        model = Event
        fields = ['author', 'title', 'description', 'link', 'dday_on',
                  'dday_on', 'dday_before', 'created_after',
                  'created_before', ]
