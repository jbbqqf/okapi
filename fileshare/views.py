# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin,
    UpdateModelMixin, DestroyModelMixin)
from rest_framework.decorators import (
    authentication_classes, permission_classes)
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import FormParser, MultiPartParser

from fileshare.models import File, Directory
from fileshare.serializers import FileSerializer, DirectorySerializer
from fileshare.permissions import (
    IsFileOwnerOrAdminOrReadOnly, CanEditDirectory)
from fileshare.filters import FileFilter, DirectoryFilter


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticatedOrReadOnly, IsFileOwnerOrAdminOrReadOnly,))
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.filter(deleted=False)
    serializer_class = FileSerializer
    parser_classes = (FormParser, MultiPartParser,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name',)
    filter_class = FileFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


def serve_private_file(request, path):
    import os
    from django.http.response import HttpResponse
    PRIVATE_MEDIA_ROOT = '/home/jbb/projects/okapi/www/private_media/'
    fullpath = os.path.join(PRIVATE_MEDIA_ROOT, path)
    response = HttpResponse()
    response['X-Sendfile'] = fullpath
    return response


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticatedOrReadOnly, CanEditDirectory,))
class DirectoryViewSet(viewsets.GenericViewSet,
                       ListModelMixin,
                       RetrieveModelMixin,
                       CreateModelMixin,
                       UpdateModelMixin,
                       DestroyModelMixin):
    """
    === Directory objects map system directories for fileshare application ===

    Directories support only alphanumeric characters and `.`, ` `, `_` and `-`
    (even if posix norm allows you some special characters).

    Directories are pure references (nothing is written on system).

    However, you cannot create or update a directory whose parent is null,
    since only preexisting root directory can have a null parent.

    There is no particular permissions to delete directories. Any logged
    user can do it but only if it's empty. If it's not, an error 400 will be
    returned. Only creators and admins can delete contained files. Root
    directory (which parent is null) is an exception that can never be
    deleted.

    ---

    list:
        parameters:
            - name: search
              description: contain filter for name
              paramType: query
              type: string

    retrieve:
        parameters:
            - name: search
              description: contain filter for content
              paramType: query
              type: string
    """

    queryset = Directory.objects.filter(deleted=False)
    serializer_class = DirectorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name',)
    filter_class = DirectoryFilter
