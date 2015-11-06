# -*- coding: utf-8 -*-

from rest_framework.pagination import PageNumberPagination


class PostsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'items'
    max_page_size = 100
