# -*- coding: utf-8 -*-

from urllib2 import (HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler,
                     build_opener, install_opener, HTTPCookieProcessor)
from cookielib import CookieJar
from requests import session


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


def init_whippet_session(login_url, user, password):
    """
    Wapiti and whippet do not use the same authent routine. Whippet pages are
    not protected with some kind of htaccess : you need to authenticate on the
    login page by giving your credentials in formdata.

    The returned session will then carry your authent token transmitted via
    http headers (well, I'm not sure about that...). The only thing you need
    to do to access any whippet page is to use this session object and call
    get or post methods (http GET and POST methods).
    """

    s = session()

    authent_formdata = {
        'username': user,
        'password': password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    s.post(
        login_url,
        data=authent_formdata,
        headers=headers,
        allow_redirects=False
    )

    return s
