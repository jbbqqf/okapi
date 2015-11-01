# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import Group as djanGroup


class Group(djanGroup):
    """
    Lots of use can be pictured for groups, even if the first goal here is to
    regroup people by promotion and by club affinity.

    An important thing to notice here is the parent field. Django's ForeignKey
    constraints do not allow such a field to be empty. Each group should have a
    parent event if it's not relevant (i.e. top-level groups such as `Fi`). For
    this reason, a virtual root group should be maintained.
    """

    url = models.CharField(max_length=100, blank=True)
    mailing = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True)

    def __unicode__(self):
        return self.name


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'url', 'mailing', 'description', 'parent', ]


# def get_group_members(group):
#     """
#     Search in manytomany relationship GroupUser model for users belonging to
#     a group given as argument. Return a list of users or an empty list.
#     """
# 
#     matches = GroupUser.objects.filter(group=group)
#     members = [member.user for member in matches]
#     return members
# 
# 
# def get_user_groups(user):
#     """
#     Search in manytomany relationship GroupUser model for groups a user given
#     as argument belongs to. Return a list of groups or an empty list.
#     """
# 
#     matches = GroupUser.objects.filter(user=user)
#     groups = [match.group for match in matches]
#     return groups
