# -*- coding: utf-8 -*-

from urllib2 import (HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler,
                     build_opener, install_opener, HTTPCookieProcessor)
from cookielib import CookieJar


def install_wapiti_opener(domain, user, passwd):
    """
    urllib2 can open pages with a default opener : no user, no password, just a
    query on an http resource. But creating a custom opener allows to give auto
    credentials and handle cookies, which we need due to the asp awful
    application implementation.
    """

    cookiejar = CookieJar()

    password_manager = HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, domain, user, passwd)
    handler = HTTPBasicAuthHandler(password_manager)

    opener = build_opener(handler, HTTPCookieProcessor(cookiejar))
    install_opener(opener)
