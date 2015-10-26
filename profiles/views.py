from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin

from profiles.filters import ProfileFilter, UserFilter
from profiles.models import Profile
from profiles.serializers import ProfileSerializer, UserSerializer
from profiles.permissions import IsProfileOwnerOrReadOnly
from groups.models import Group
from groups.serializers import GroupSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    === Provide basic informations about students from Telecom's LDAP ===

    The route ~/users/ aims to provide basic informations about students
    extracted from the school's LDAP directory. User objects are django's user.
    That's why not much information is provided. If you want more about users
    you should check users profiles.

    is_staff field mean admin field in django's terms.

    Thoses informations are read-only API wise, even for admins. If you really
    want to manually edit a user (ie: is_staff field) you have to do it via the
    django admin interface (it requires to be a staff member). Do not intend to
    edit those informations without knowing what you are doing.

    ---

    list:
        parameters:
            - name: search
              description: contain filter for first_name or last_name
                           (multiple values separated by `,`)
              paramType: query
              type: string

    retrieve:
        parameters:
            - name: search
              description: contain filter for first_name or last_name
                           (multiple values separated by `,`)
              paramType: query
              type: string
    """

    queryset = User.objects.exclude(id=-1)
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('first_name', 'last_name',)
    filter_class = UserFilter

    # @detail_route()
    # def groups(self, request, pk=None):
    #     """
    #     This route allows to request all groups a user belongs to.
    #     """

    #     user = self.get_object()

    #     groups = get_user_groups(user)
    #     
    #     serializer = GroupSerializer(groups, many=True)
    #     return Response(serializer.data)

@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly,))
class ProfileViewSet(ListModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    === Profiles bring additional informations about users ===
    
    The main difference between ~/profiles/ and ~/users/ route is that users can
    edit their profiles but cannot change their core account informations.

    Only profile owner can perform PUT or PATCH requests. POST is not allowed
    because your profile is supposed to be unique and created when you log in
    for the first time.

    ---

    list:
        parameters:
            - name: search
              description: contain filter for nick or note (multiple values
                           separated by `,`)
              paramType: query
              type: string

    retrieve:
        parameters:
            - name: search
              description: contain filter for nick or note (multiple values
                           separated by `,`)
              paramType: query
              type: string
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('nick', 'note',)
    filter_class = ProfileFilter
