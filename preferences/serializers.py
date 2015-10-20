from rest_framework import serializers
from preferences.models import UserInterface, UserTheme

class UserInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterface
        read_only_fields = ['name', 'comment',]

class UserThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTheme
        fields = ['user',]
