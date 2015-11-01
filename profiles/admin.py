# -*- coding: utf-8 -*-

from django.contrib.admin import ModelAdmin
from django.contrib.admin.site import register
from profiles.models import Profile, ProfileForm


class ProfileAdmin(ModelAdmin):
    form = ProfileForm
    list_display = ['nick', 'birthday', 'note', 'gender', 'user', ]
    search_fields = ['nick', 'birthday', 'note', ]

register(Profile, ProfileAdmin)
