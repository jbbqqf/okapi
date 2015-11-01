# -*- coding: utf-8 -*-

from django.contrib.admin import ModelAdmin
from django.contrib.admin.site import register
from fileshare.models import File, FileForm, Directory, DirectoryForm


class DirectoryAdmin(ModelAdmin):
    form = DirectoryForm
    list_display = ['name', 'parent', 'deleted', 'created', 'modified', ]


class FileAdmin(ModelAdmin):
    form = FileForm
    list_display = [
        'name', 'parent', 'creator', 'deleted', 'created', 'modified', ]

register(Directory, DirectoryAdmin)
register(File, FileAdmin)
