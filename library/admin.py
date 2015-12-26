# -*- coding: utf-8 -*-

from django.contrib import admin
from library.models import PressReview, PressReviewForm


class PressReviewAdmin(admin.ModelAdmin):
    form = PressReviewForm
    list_display = ('date', 'link',)
    search_fields = ('date',)

admin.site.register(PressReview, PressReviewAdmin)
