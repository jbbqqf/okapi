# -*- coding: utf-8 -*-

from urllib2 import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, HTTPError
from rest_framework import serializers, exceptions

class MyGradesSerializer(serializers.Serializer):
    wapiti_username = serializers.CharField(max_length=30)
    wapiti_password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        user = attrs.get('wapiti_username')
        passwd = attrs.get('wapiti_password')

        if not(user and passwd):
            error = 'You need to provide a valid wapiti username and password'
            raise exceptions.ValidationError(error)

        domain = 'https://wapiti.telecom-lille.fr'
        authelv = '{}/authelv.php'.format(domain)

        passwd_manager = HTTPPasswordMgrWithDefaultRealm()
        passwd_manager.add_password(None, domain, user, passwd)
        handler = HTTPBasicAuthHandler(passwd_manager)
        opener = build_opener(handler)

        try:
            opener.open(authelv)
        except HTTPError:
            error = 'Could not open {} with provided login data'.format(authelv)
            if not user.startswith('elv/'):
                error += ' (did you forget `elv/` before username ?)'

            raise exceptions.ValidationError(error)

        return attrs
