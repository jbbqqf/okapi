# -*- coding: utf-8 -*-

from django.contrib import admin
from button.models import Clear, ClearForm


class ClearAdmin(admin.ModelAdmin):
    form = ClearForm
    list_display = ('id', 'user', 'date',)
    search_fields = ('user__username',)

admin.site.register(Clear, ClearAdmin)
