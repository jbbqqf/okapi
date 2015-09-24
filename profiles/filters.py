# -*- coding: utf-8 -*-

from django_filters import FilterSet, CharFilter, DateFilter, MethodFilter, BooleanFilter, NumberFilter
from profiles.models import Profile
from groups.models import Group, GroupUser
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class UserFilter(FilterSet):
    firstname = CharFilter(name='first_name', lookup_type='icontains',
                           label='first_name contain filter')
    lastname = CharFilter(name='last_name', lookup_type='icontains',
                          label='last_name contain filter')
    is_staff = BooleanFilter(name='is_staff', label='is admin ?')
    glabel = 'filter users who belong to group whose name exactly match value'
    group = MethodFilter(action='group_filter', label=glabel)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'is_staff', 'group',]

    def group_filter(self, queryset, value):
        """
        Filtering users by group could be easy if matching test is about ids.
        But it's easier to search by names. Since relations between users and
        groups require manytomany records, this method makes the job.

        Django models support native manytomany relationships, but it's not that
        easy with django rest framework.
        """

        # Provided value might not match anything. If it's the case this filter
        # tests for exact matches. It could be improved...
        try:
            group = Group.objects.get(name=value)
        except ObjectDoesNotExist:
            return None

        group_users = GroupUser.objects.filter(group=group)
        users_in_group = [gu.user for gu in group_users]
        
        return users_in_group

class ProfileFilter(FilterSet):
    nick = CharFilter(name='nick', lookup_type='icontains',
                      label='nick contain filter')
    born_after = DateFilter(name='birthday', lookup_type='gte',
                            label='users who are born after or on value')
    born_before = DateFilter(name='birthday', lookup_type='lte',
                             label='users who are born before or on value')
    born_on = DateFilter(name='birthday',
                         label='users who are born on provided value')
    note = CharFilter(name='note', lookup_type='icontains',
                      label='note contain filter')
    gender = CharFilter(name='gender', label='filter on gender value')
    user = NumberFilter(name='user', label='user whose id is provided value')

    class Meta:
        model = Profile
        fields = ['nick', 'born_after', 'born_before', 'born_on', 'note', 'gender', 'user',]
