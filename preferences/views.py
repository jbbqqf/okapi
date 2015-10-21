from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication

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

@authentication_classes((TokenAuthentication, SessionAuthentication, BasicAuthentication,))
@permission_classes((IsAuthenticated,))
class UserPrefView(ListModelMixin,
                    RetrieveModelMixin,
                    GenericViewSet):
    """
    === Allows a user to access his saved themes ===
    """

    serializer_class = UserPrefSerializer

    def get_queryset(self):
        queryset = UserPref.objects.filter(user=self.request.user)
        return queryset

