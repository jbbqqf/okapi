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

from profiles.filters import ProfileFilter, UserFilter
from profiles.models import Profile
from profiles.serializers import ProfileSerializer, UserSerializer
from profiles.permissions import IsProfileOwnerOrReadOnly
from groups.models import Group, GroupUser
from groups.serializers import GroupSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('first_name', 'last_name',)
    filter_class = UserFilter

    @detail_route()
    def groups(self, request, pk=None):
        user = self.get_object()
        user_groups = GroupUser.objects.filter(user=user.id)

        groups = []
        for user_group in user_groups:
            groups.append(Group.objects.get(id=user_group.group.id))

        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly,))
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'put', 'patch', 'head', 'options',]
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('nick', 'note',)
    filter_class = ProfileFilter
