# -*- coding: utf-8 -*-

from django.contrib import admin
from groups.models import Group, GroupForm


class GroupAdmin(admin.ModelAdmin):
    form = GroupForm
    list_display = ['id', 'name', 'url', 'mailing', 'description', 'parent']
    search_fields = ['name', 'url', 'mailing', 'description', 'parent']

admin.site.register(Group, GroupAdmin)
