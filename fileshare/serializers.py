# -*- coding: utf-8 -*-

from rest_framework import serializers
from fileshare.models import File, Directory

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'parent',)

class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = ('id', 'name', 'parent',)
