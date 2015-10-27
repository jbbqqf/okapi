from django.shortcuts import render
from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.filters import DjangoFilterBackend, SearchFilter

from preferences.filters import UserInterfaceFilter, UserPrefFilter
from preferences.models import UserInterface, UserPref
from preferences.serializers import UserInterfaceSerializer, UserPrefSerializer

@authentication_classes((TokenAuthentication, SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
class UserInterfaceView(ListModelMixin,
                        RetrieveModelMixin,
                        GenericViewSet):
    """
    === A list of all known user interfaces ===
    """

    queryset = UserInterface.objects.all()
    serializer_class = UserInterfaceSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name', 'comment',)
    filter_class = UserInterfaceFilter

@authentication_classes((TokenAuthentication, SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
class UserPrefView(ListModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    """
    === Allows a user to access his saved themes ===
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
