# -*- coding: utf-8 -*-

from django.db.models import (Model, ForeignKey, DateTimeField)
from django.forms import ModelForm

from django.contrib.auth.models import User


class Clear(Model):
    """
    Press the button !
    """

    user = ForeignKey(User)
    date = DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{} cleared {}'.format(self.user, self.date)


class ClearForm(ModelForm):
    class Meta:
        model = Clear
        fields = ('user',)
