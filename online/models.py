# -*- coding: utf-8 -*-

from django.db.models import (
    Model, OneToOneField, DateTimeField, BooleanField, GenericIPAddressField)
from django.forms import ModelForm
from django.contrib.auth.models import User


class Presence(Model):
    """
    User interfaces decide when to push which information and whether they want
    to use stuff here. Since okapi is a stateless web service and can handle
    multiple clients, there is no way to force users to show themselves.

    However, if the implementation wants to offer this feature to make chat
    discussions more convenient, Presence objects offer this possibility.

    The last_active field should be updated frequently to inform that
    connected user has used his mouse, clicked or triggered something on the
    interface. If the interface environment allows it, a running client can
    also update it to inform that his user is still connected but hasn't been
    active.
    """

    user = OneToOneField(User)
    last_passive = DateTimeField(blank=True, null=True)
    last_active = DateTimeField(blank=True, null=True)
    # Clients can allow or not to push those personnal informations
    ip = GenericIPAddressField(blank=True, null=True)
    proxy_ip = GenericIPAddressField(blank=True, null=True)
    # Users can toggle this to True/False
    away = BooleanField(default=False)


class PresenceForm(ModelForm):
    class Meta:
        model = Presence
        fields = (
            'user',
            'last_passive',
            'last_active',
            'ip',
            'proxy_ip',
            'away',
        )
