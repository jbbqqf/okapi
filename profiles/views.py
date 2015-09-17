from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from profiles.models import Profile
from profiles.serializers import ProfileSerializer, UserSerializer
from profiles.permissions import IsProfileOwnerOrReadOnly

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly,))
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'put', 'patch', 'head', 'options',]
