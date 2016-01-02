# -*- coding: utf-8 -*-

from django.contrib import admin
from score.models import Score, ScoreForm, CurrentScore, CurrentScoreForm


class ScoreAdmin(admin.ModelAdmin):
    form = ScoreForm
    list_display = ('user', 'game', 'value', 'date',)
    search_fields = ('user__username', 'game', 'value',)


class CurrentScoreAdmin(admin.ModelAdmin):
    form = CurrentScoreForm
    list_display = ('user', 'value',)
    search_fields = ('user__username', 'value',)

admin.site.register(Score, ScoreAdmin)
admin.site.register(CurrentScore, CurrentScoreAdmin)
