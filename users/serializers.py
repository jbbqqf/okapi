# -*- coding: utf-8 -*-

from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('login', 'profile_id', 'locked')
