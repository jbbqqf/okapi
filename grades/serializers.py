# -*- coding: utf-8 -*-

from urllib2 import (HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler,
                     build_opener, HTTPError)
from rest_framework.serializers import Serializer, CharField
from rest_framework.exceptions import ValidationError


class WapitiLoginSerializer(Serializer):
    """
    Serialize and validate wapiti platform login credentials. Wapiti and Okapi
    credentials will often be the same, but it is not an obligation (ie.
    graduates or people who didn't synchronized their password).

    wapiti_ prefix on username/password reminds that you need to prefix your
    username by `elv/` domain. We could auto-prefix username by `elv/`) but
    this kind of automatisation is more likely to be handled on user interface
    than on backend.
    """

    wapiti_username = CharField(max_length=30)
    wapiti_password = CharField(max_length=128)

    def validate(self, attrs):
        """
        Validating those login datas is made by trying to open an accessible
        wapiti url. If the page can be downloaded, it is validated.
        """

        user = attrs.get('wapiti_username')
        passwd = attrs.get('wapiti_password')

        if not(user and passwd):
            error = 'You need to provide a valid wapiti username and password'
            raise ValidationError(error)

        domain = 'https://wapiti.telecom-lille.fr'
        authelv = '{}/authelv.php'.format(domain)

        passwd_manager = HTTPPasswordMgrWithDefaultRealm()
        passwd_manager.add_password(None, domain, user, passwd)
        handler = HTTPBasicAuthHandler(passwd_manager)
        opener = build_opener(handler)

        try:
            opener.open(authelv)

        # HTTPError is not very precise here. It could be wrong credentials as
        # well as any other error (DNS resolving, unavailable resource...).
        # TODO: try to handle errors more precisely even if wrong credentials
        # appears to be the most common one.
        except HTTPError:
            error = 'Could not open {} with provided login data'.format(
                authelv)
            if not user.startswith('elv/'):
                error += ' (did you forget `elv/` before username ?)'

            raise ValidationError(error)

        return attrs
