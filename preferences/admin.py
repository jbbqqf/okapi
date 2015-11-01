# -*- coding: utf-8 -*-

from django.contrib.admin import ModelAdmin
from django.contrib.admin.site import register
from preferences.models import (
    UserInterface, UserInterfaceForm, UserPref, UserPrefForm)


class UserInterfaceAdmin(ModelAdmin):
    form = UserInterfaceForm
    list_display = ['name', 'comment', ]
    search_fields = ['name', 'comment', ]


class UserPrefAdmin(ModelAdmin):
    form = UserPrefForm
    list_display = ['user', 'ui', 'conf', ]
    search_fields = ['user', 'ui', 'conf', ]

register(UserInterface, UserInterfaceAdmin)
register(UserPref, UserPrefAdmin)
