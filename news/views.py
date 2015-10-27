from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.filters import DjangoFilterBackend, SearchFilter

from news.models import Event
from news.serializers import EventSerializer
from news.filters import EventFilter
from news.permissions import IsEventAuthorOrAdminOrReadOnly

@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticatedOrReadOnly, IsEventAuthorOrAdminOrReadOnly,))
class EventView(ModelViewSet):
    """
    === Create and share events of your BDE and other organizations ! ===

    Only connected users can create events but you don't need to be connected
    to read it. Only an event author or a user admin with is_staff property set
    to true can PUT / DELETE his event.

    author and created fields are added automaticaly on an event creation.

    link should be an url (not more than 255 characters) but can be anything
    else...

    ---

    list:
        parameters:
            - name: search
              description: contain filter for author's name, title, description
                           and link
              paramType: query
              type: string

    retrieve:
        parameters:
            - name: search
              description: contain filter for author's name, title, description
                           and link
              paramType: query
              type: string
    """
    
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ['author__username', 'title', 'description', 'link',]
    filter_class = EventFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
