# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, StringRelatedField
from profiles.models import Profile, PhoneNumber, Email, SocialNetwork


class PhoneNumberSerializer(ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['number', ]


class EmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        fields = ['email', ]


class SocialNetworkSerializer(ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ['network', 'link', ]


class ProfileSerializer(ModelSerializer):
    tels = StringRelatedField(many=True, read_only=True)
    mails = StringRelatedField(many=True, read_only=True)
    social_networks = SocialNetworkSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        read_only_fields = ['user', ]
        fields = ['id', 'user', 'birthday', 'note', 'gender', 'tels', 'mails',
                  'social_networks', ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'date_joined', ]
