# -*- coding: utf-8 -*-

from django_filters import FilterSet, NumberFilter, DateFilter
from button.models import Clear


class ClearFilter(FilterSet):
    user = NumberFilter(name='user',
                        label='user whose id is provided value')
    date_on = DateFilter(name='date',
                         label='buttons cleared on value')
    date_after = DateFilter(name='date', lookup_type='gte',
                            label='buttons cleared after or on value')
    date_before = DateFilter(name='date', lookup_type='lte',
                             label='buttons cleared before or on value')

    class Meta:
        model = Clear
        fields = (
            'user',
            'date_on',
            'date_after',
            'date_before',
        )
