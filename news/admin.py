# -*- coding: utf-8 -*-

from django.contrib.admin import ModelAdmin
from django.contrib.admin.site import register
from news.models import Event, EventForm


class EventAdmin(ModelAdmin):
    form = EventForm
    list_display = ['author', 'title', 'description', 'link', 'created',
                    'dday', 'visible', ]
    search_fields = ['author', 'title', 'description', 'link', 'dday', ]

register(Event, EventAdmin)
