# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import (
    ModelSerializer, HyperlinkedModelSerializer, StringRelatedField,
    SerializerMethodField)
from profiles.models import Profile, PhoneNumber, Email, SocialNetwork


class PhoneNumberSerializer(ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('number',)


class EmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        fields = ('email',)


class SocialNetworkSerializer(ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ('network', 'link',)


class ProfileSerializer(ModelSerializer):
    tels = StringRelatedField(many=True, read_only=True)
    mails = StringRelatedField(many=True, read_only=True)
    social_networks = SocialNetworkSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        read_only_fields = ('user',)
        fields = (
            'id',
            'user',
            'birthday',
            'note',
            'gender',
            'tels',
            'mails',
            'social_networks',
        )


class UserSerializer(HyperlinkedModelSerializer):
    profile = SerializerMethodField()

    def get_profile(self, user):
        try:
            return user.profile.id

        except ObjectDoesNotExist:
            return None

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'profile',
            'date_joined',
        )
