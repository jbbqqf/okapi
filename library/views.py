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
from library.pagination import PressReviewPagination


@authentication_classes((TokenAuthentication, SessionAuthentication,))
@permission_classes((IsAuthenticated,))
class PressReviewView(ReadOnlyModelViewSet):
    """
    === Supply whippet press reviews links to download it ===

    On whippet you can find an interesting section of the library page
    containing press reviews. It has not been advertised and the pressreviews
    route aims to highlight those reviews.

    Those press reviews objects do not contain any press review itself, but it
    records dates on which a given press review has been made and the relative
    link to download it from telnew server local storage.
    """

    queryset = PressReview.objects.all()
    serializer_class = PressReviewSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ['date', ]
    filter_class = PressReviewFilter
    pagination_class = PressReviewPagination

    @list_route(methods=['get'])
    def today(self, request):
        """
        === Today's press review or an empty list ===
        """

        today_press_review = PressReview.objects.filter(
            date=strftime('%Y-%m-%d'))
        serializer = self.get_serializer(today_press_review, many=True)

        return Response(serializer.data)
