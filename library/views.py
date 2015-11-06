# -*- coding: utf-8 -*-

from time import strftime

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication, SessionAuthentication)
from rest_framework.decorators import (
    authentication_classes, permission_classes, list_route)
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework.response import Response

from library.models import PressReview
from library.serializers import PressReviewSerializer
from library.filters import PressReviewFilter


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
class PressReviewView(ReadOnlyModelViewSet):
    queryset = PressReview.objects.all()
    serializer_class = PressReviewSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ['date', ]
    filter_class = PressReviewFilter

    @list_route(methods=['get'])
    def today(self, request):
        today_press_review = PressReview.objects.filter(
            date=strftime('%Y-%m-%d'))
        serializer = self.get_serializer(today_press_review, many=True)

        return Response(serializer.data)
