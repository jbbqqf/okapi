# -*- coding: utf-8 -*-

from django_filters import FilterSet, CharFilter, NumberFilter, MethodFilter
from preferences.models import UserPref, UserInterface


class UserInterfaceFilter(FilterSet):
    name = CharFilter(name='name', lookup_type='icontains',
                      label='name contain filter')
    comment = CharFilter(name='comment', lookup_type='icontains',
                         label='comment contain filter')

    class Meta:
        model = UserInterface
        fields = ['name', 'comment', ]


class UserPrefFilter(FilterSet):
    ui_id = NumberFilter(name='ui',
                         label='filter preference by ui with its id')
    ui = MethodFilter(action='ui_name_filter',
                      label='ui name contain filter')
    conf = CharFilter(name='conf', lookup_type='icontains',
                      label='conf contain filter')

    def ui_name_filter(self, queryset, value):
        return queryset.filter(ui__name__icontains=value)

    class Meta:
        model = UserPref
        fields = ['ui_id', 'ui', 'conf', ]
