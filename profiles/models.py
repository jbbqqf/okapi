# -*- coding: utf-8 -*-

from django.db.models import (
    Model, DateField, TextField, CharField, ForeignKey)
from django.forms import ModelForm
from django.contrib.auth.models import User


class Profile(Model):
    """
    Profiles provide some extra informations about it's user. Those fields are
    generic and should be enough in a first time. If you want to add other
    fields (avatar for instance), you should create a new app to avoid breaking
    retro-compatibility. Or if you do so, make sure it has minor impact on UIs.

    Fields like custom e-mail or mobile have been intentionnaly not provided
    because it's more likely a manytomany relation.
    """

    GENDER = [
        ('n', 'na'),
        ('m', 'man'),
        ('w', 'woman'),
        ('u', 'unknown'),
    ]

    nick = CharField(max_length=24)
    birthday = DateField(blank=True, null=True)
    note = TextField(blank=True)
    gender = CharField(max_length=1, choices=GENDER, default=GENDER[0][0])
    user = ForeignKey(User)

    def __unicode__(self):
        return u'{}\'s profile'.format(self.user.username)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['nick', 'birthday', 'note', 'gender', 'user', ]
