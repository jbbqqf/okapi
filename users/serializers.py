# -*- coding: utf-8 -*-

from rest_framework import serializers
from users.models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('login', 'profile_id', 'locked')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
