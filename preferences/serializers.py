from rest_framework import serializers
from preferences.models import UserInterface, UserPref

class UserInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterface
        read_only_fields = ['name', 'comment',]

class UserPrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPref
        read_only_fields = ['user',]
        fields = ['id', 'user', 'ui', 'conf',]
