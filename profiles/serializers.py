# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from profiles.models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        read_only_fields = ['user', ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'date_joined', ]
