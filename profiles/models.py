# -*- coding: utf-8 -*-

from django.db.models import (
    Model, DateField, TextField, CharField, EmailField, ManyToManyField,
    OneToOneField)
from django.forms import ModelForm
from django.contrib.auth.models import User


class PhoneNumber(Model):
    """
    Handle ManyToManyField tels on Profile

    Do you want her 06 ?..
    """

    number = CharField(max_length=16)

    def __unicode__(self):
        return self.number


class PhoneNumberForm(ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['number', ]


class Email(Model):
    """
    Handle ManyToManyField mails on Profile
    """

    email = EmailField()

    def __unicode__(self):
        return self.email


class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ['email', ]


class SocialNetwork(Model):
    """
    Handle ManyToManyField social_networks on Profile.

    A social network is the association of a network name and a link to the
    user profile.
    """

    NETWORKS = [
        ('fb', 'facebook'),
        ('tw', 'twitter'),
        ('g+', 'google+'),
        ('li', 'linkedin'),
        ('ti', 'tindr'),
    ]

    network = CharField(max_length=2, choices=NETWORKS)
    link = CharField(max_length=256)

    def __unicode__(self):
        return u'{}: {}'.format(self.network, self.link)


class SocialNetworkForm(ModelForm):
    class Meta:
        model = SocialNetwork
        fields = ['network', 'link', ]


class Profile(Model):
    """
    Profiles provide some extra informations about it's user. Those fields are
    generic and should be enough in a first time. If you want to add other
    fields (avatar for instance), you should create a new app to avoid breaking
    retro-compatibility. Or if you do so because you think it has been
    forgotten but should be part of the profile core, make sure to notify UI
    developers.
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
    tels = ManyToManyField(PhoneNumber, blank=True)
    mails = ManyToManyField(Email, blank=True)
    social_networks = ManyToManyField(SocialNetwork, blank=True)
    user = OneToOneField(User)

    def __unicode__(self):
        return u'{}\'s profile'.format(self.user.username)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'nick', 'birthday', 'note', 'gender', 'tels',
                  'mails', 'social_networks', ]
