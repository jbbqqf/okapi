# -*- coding: utf-8 -*-

from django.contrib import admin
from online.models import Presence, PresenceForm


class PresenceAdmin(admin.ModelAdmin):
    form = PresenceForm
    list_display = (
        'user',
        'last_passive',
        'last_active',
        'away',
    )
    search_fields = ('user__username',)

admin.site.register(Presence, PresenceAdmin)
