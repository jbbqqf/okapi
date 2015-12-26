# -*- coding: utf-8 -*-

from django.contrib import admin
from fileshare.models import File, FileForm, Directory, DirectoryForm


class DirectoryAdmin(admin.ModelAdmin):
    form = DirectoryForm
    list_display = ['name', 'parent', 'deleted', 'created', 'modified', ]


class FileAdmin(admin.ModelAdmin):
    form = FileForm
    list_display = (
        'name',
        'parent',
        'file',
        'creator',
        'deleted',
        'created',
        'modified',
    )

admin.site.register(Directory, DirectoryAdmin)
admin.site.register(File, FileAdmin)
