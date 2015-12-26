# -*- coding: utf-8 -*-

from django_filters import FilterSet, DateTimeFilter
from library.models import PressReview


class PressReviewFilter(FilterSet):
    po_label = 'filter press reviews published on provided date'
    published_on = DateTimeFilter(name='date', label=po_label)
    pa_label = 'filter press reviews published after provided date'
    published_after = DateTimeFilter(name='date', lookup_type='gte',
                                     label=pa_label)
    pb_label = 'filter press reviews published before provided date'
    published_before = DateTimeFilter(name='date', lookup_type='lte',
                                      label=pb_label)

    class Meta:
        model = PressReview
        fields = ('published_on', 'published_after', 'published_before',)
