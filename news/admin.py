# -*- coding: utf-8 -*-

from django.contrib import admin
from news.models import Event, EventForm


class EventAdmin(admin.ModelAdmin):
    form = EventForm
    list_display = ['author', 'title', 'description', 'link', 'created',
                    'dday', 'visible', ]
    search_fields = ['author', 'title', 'description', 'link', 'dday', ]

admin.site.register(Event, EventAdmin)
