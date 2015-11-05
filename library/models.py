# -*- coding: utf-8 -*-

from django.db.models import (Model, DateField, CharField)
from django.forms import ModelForm


class PressReview(Model):
    date = DateField()
    link = CharField(max_length=255)

    def __unicode__(self):
        return '{} press review'.format(self.date)


class PressReviewForm(ModelForm):
    class Meta:
        model = PressReview
        fields = ['date', 'link', ]
