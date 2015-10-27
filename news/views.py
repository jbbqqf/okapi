from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes

from news.models import Event
from news.serializers import EventSerializer

@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly,))
class EventView(ModelViewSet):
    
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
