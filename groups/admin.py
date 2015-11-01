# -*- coding: utf-8 -*-

from django.contrib.admin import ModelAdmin
from django.contrib.admin.site import register
from groups.models import Group, GroupForm


class GroupAdmin(ModelAdmin):
    form = GroupForm
    list_display = ['id', 'name', 'url', 'mailing', 'description', 'parent']
    search_fields = ['name', 'url', 'mailing', 'description', 'parent']

register(Group, GroupAdmin)
