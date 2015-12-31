# -*- coding: utf-8 -*-

from django_filters import (
    FilterSet, NumberFilter, DateFilter, BooleanFilter, CharFilter)
from online.models import Presence


class PresenceFilter(FilterSet):
    user = NumberFilter(name='user', label='user whose id is provided value')
    passive_after_label = 'users who were connected after or on value'
    passive_after = DateFilter(name='last_passive', lookup_type='gte',
                               label=passive_after_label)
    passive_before_label = 'users who were connected before or on value'
    passive_before = DateFilter(name='last_passive', lookup_type='lte',
                                label=passive_before_label)
    active_after_label = 'users who were active after or on value'
    active_after = DateFilter(name='last_active', lookup_type='gte',
                              label=active_after_label)
    active_before_label = 'users who were active before or on value'
    active_before = DateFilter(name='last_active', lookup_type='lte',
                               label=active_before_label)
    ip = CharFilter(name='ip', lookup_type='icontains',
                    label='ip contain filter')
    proxy_ip = CharFilter(name='proxy_ip', lookup_type='icontains',
                          label='proxy_ip contain filter')
    away = BooleanFilter(name='away', label='is away ?')

    class Meta:
        model = Presence
        fields = (
            'user',
            'passive_after',
            'passive_before',
            'active_after',
            'active_before',
            'ip',
            'proxy_ip',
            'away',
        )
