# -*- coding: utf-8 -*-

from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    authentication_classes, permission_classes)
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.filters import DjangoFilterBackend, SearchFilter

from preferences.filters import UserInterfaceFilter, UserPrefFilter
from preferences.models import UserInterface, UserPref
from preferences.serializers import UserInterfaceSerializer, UserPrefSerializer


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
class UserInterfaceView(ListModelMixin,
                        RetrieveModelMixin,
                        GenericViewSet):
    """
    === A list of all known user interfaces ===

    Those objects are readonly API-wise. If you need to add your own entry, you
    should contact an admin.

    ---

    list:
        parameters:
            - name: search
              description: contain filter for name and comment
              paramType: query
              type: string

    retrieve:
        parameters:
            - name: search
              description: contain filter for name and comment
              paramType: query
              type: string
    """

    queryset = UserInterface.objects.all()
    serializer_class = UserInterfaceSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name', 'comment',)
    filter_class = UserInterfaceFilter


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
class UserPrefView(ListModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    """
    === Allows a user to access his saved prefs ===

    An authenticated user can only GET, POST or PATCH his own preferences.

    All users do not need to have custom preferences. You should create a new
    entry only for users who changed something from the default preferences.
    When retrieving user preferences, if you get nothing, you know this user
    has default preferences.

    A constraint prevents any user to have two different preferences for a
    given user interface. It means you filter entries by ui_id, you should
    always have only one entry. But BE CAREFUL : user interface ids are not
    guaranteed to be constant over time (if database is migrated for example),
    even if it won't happen often.

    A good practice when you manipulate user preferences if you want to be
    100% sure of what you recieve is to filter your results both by id and user
    interface name. It should be tested by the interface, and if one fails you
    can just use default parameters instead of running the risk to use
    corrupted data.

    ---

    list:
        parameters:
            - name: search
              description: contain filter for ui's name and conf
              paramType: query
              type: string

    retrieve:
        parameters:
            - name: search
              description: contain filter for ui's name and conf
              paramType: query
              type: string
    """

    serializer_class = UserPrefSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('ui__name', 'conf',)
    filter_class = UserPrefFilter

    def get_queryset(self):
        queryset = UserPref.objects.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)

        except IntegrityError:
            error = {'message': 'Duplicate entry for user {} and ui {}'.format(
                self.request.user, serializer.validated_data['ui'])}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        You can only create preferences for your account.
        """

        serializer.save(user=self.request.user)
