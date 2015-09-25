from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.filters import DjangoFilterBackend, SearchFilter

from fileshare.models import File, Directory
from fileshare.serializers import FileSerializer, DirectorySerializer
from fileshare.filters import FileFilter, DirectoryFilter

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.filter(deleted=False)
    serializer_class = FileSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name',)
    filter_class = FileFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class DirectoryViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.filter(deleted=False)
    serializer_class = DirectorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name',)
    filter_class = DirectoryFilter
