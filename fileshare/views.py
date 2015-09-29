from os.path import join
from os import makedirs

from django.db import transaction
from django.shortcuts import render
from django.conf import settings

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
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

    def create(self, request, pk=None):
        serializer = DirectorySerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    new_dir = serializer.save()
                    makedirs(join(settings.MEDIA_ROOT,
                                  'fileshare',
                                  new_dir.to_relative()))
            except OSError as e:
                error = {'message': 'Server could not create directory'}
                return Response(error,
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
