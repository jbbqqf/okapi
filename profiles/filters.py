# -*- coding: utf-8 -*-

from django_filters import FilterSet, CharFilter, DateFilter, MethodFilter
from profiles.models import Profile
from groups.models import Group, GroupUser
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class UserFilter(FilterSet):
    firstname = CharFilter(name='first_name', lookup_type='icontains')
    lastname = CharFilter(name='last_name', lookup_type='icontains')
    group = MethodFilter(action='group_filter')
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'is_staff', 'group',]

    def group_filter(self, queryset, value):
        try:
            group = Group.objects.get(name=value)
        except ObjectDoesNotExist:
            return None
        group_users = GroupUser.objects.filter(group=group)
        users_in_group = [gu.user for gu in group_users]
        
        return users_in_group

class ProfileFilter(FilterSet):
    nick = CharFilter(name='nick', lookup_type='icontains')
    born_after = DateFilter(name='birthday', lookup_type='gte')
    born_before = DateFilter(name='birthday', lookup_type='lte')
    born_on = DateFilter(name='birthday')
    note = CharFilter(name='note', lookup_type='icontains')
    class Meta:
        model = Profile
        fields = ['nick', 'born_after', 'born_before', 'born_on', 'note', 'gender', 'user',]
