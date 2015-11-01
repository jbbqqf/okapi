# -*- coding: utf-8 -*-

from django.db.models import (Model, ForeignKey, CharField, TextField,
                              DateField, DateTimeField, BooleanField)
from django.forms import ModelForm, CharField as formCharField, Textarea
from django.contrib.auth.models import User


class Event(Model):
    author = ForeignKey(User)

    title = CharField(max_length=32)
    description = TextField(null=True)
    link = CharField(max_length=255, null=True)

    created = DateTimeField(auto_now_add=True)
    dday = DateField()

    visible = BooleanField(default=True)

    def __unicode__(self):
        return '{} on {}'.format(self.title, self.dday)


class EventForm(ModelForm):
    description = formCharField(required=False, widget=Textarea)
    link = formCharField(max_length=255, required=False)

    class Meta:
        model = Event
        fields = ['author', 'title', 'description', 'link', 'dday', ]
