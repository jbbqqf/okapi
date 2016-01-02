# -*- coding: utf-8 -*-

from django_filters import FilterSet, CharFilter, NumberFilter, DateFilter
from score.models import Score, CurrentScore


class ScoreFilter(FilterSet):
    user = NumberFilter(name='user',
                        label='user whose id is provided value')
    game = CharFilter(name='game', label='scores whose game name is value')
    value = NumberFilter(name='value',
                         label='current scores being equal to value')
    value_gte_label = 'current scores being greater or equal to value'
    value_gte = NumberFilter(name='value', lookup_type='gte',
                             label=value_gte_label)
    value_lte_label = 'current scores being lower or equal to value'
    value_lte = NumberFilter(name='value', lookup_type='lte',
                             label=value_lte_label)
    date_after = DateFilter(name='date', lookup_type='gte',
                            label='scores scored after or on value')
    date_before = DateFilter(name='date', lookup_type='lte',
                             label='scores scored before or on value')
    date_on = DateFilter(name='date',
                         label='scores scored on value')

    class Meta:
        model = Score
        fields = (
            'user',
            'game',
            'value',
            'value_gte',
            'value_lte',
            'date_after',
            'date_before',
            'date_on',
        )


class CurrentScoreFilter(FilterSet):
    user = NumberFilter(name='user',
                        label='usre whose id is provided value')
    value = NumberFilter(name='value',
                         label='current scores being equal to value')
    value_gte_label = 'current scores being greater or equal to value'
    value_gte = NumberFilter(name='value', lookup_type='gte',
                             label=value_gte_label)
    value_lte_label = 'current scores being lower or equal to value'
    value_lte = NumberFilter(name='value', lookup_type='lte',
                             label=value_lte_label)

    class Meta:
        model = CurrentScore
        fields = (
            'user',
            'value',
            'value_gte',
            'value_lte',
        )
