# -*- coding: utf-8 -*-

from os.path import join
from django.conf import settings
from django.http import HttpResponse

from rest_framework.authtoken.models import Token


def is_allowed(request):
    try:
        auth_headers = request.META.get('HTTP_AUTHORIZATION')
        auth_token = auth_headers.split(' ')
        assert (auth_token[0] == 'Token'), \
            "Token should be announced with a `Token ` string"
        Token.objects.get(key=auth_token[1])
        return True

    except:
        return False


def serve_private_media(request, path):
    if is_allowed(request):
        fullpath = join(settings.PRIVATE_MEDIA_ROOT, path)
        response = HttpResponse()
        response['X-Sendfile'] = fullpath
        return response

    else:
        return HttpResponse('Unauthorized', status=401)
