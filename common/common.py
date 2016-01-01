# -*- include: utf-8 -*-

from subprocess import Popen, PIPE


def cmd(*args):
    """Execute a shell command"""

    return Popen(args, stdout=PIPE, stderr=PIPE).communicate()[0]


def find_string_between(string, sub_first, sub_last):
    """
    Common function to find a substring surrounded by sub_first and sub_last.
    sub_last can be set to None if for example you expect to isolate something
    at the end of the string. In this case, the whole string after sub_first is
    returned.

    In case submitted data raises a ValueError, an empty string will be
    returned instead.
    """

    try:
        start = string.index(sub_first) + len(sub_first)
        if sub_last is not None:
            end = string.index(sub_last, start)
            return string[start:end]

        else:
            return string[start:]

    except ValueError:
        return ''


def get_ip(request):
    """
    Returns the IP of the request, accounting for the possibility of being
    behind a proxy, or None if not able to read it.

    cf https://www.djangosnippets.org/snippets/2575/
    """

    ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ip:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ip = ip.split(', ')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip


def get_first_proxy_ip(request):
    """
    Returns the IP of the first proxy of the request or None.
    """

    proxies = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if proxies:
        proxy_ips = proxies.split(', ')
        if len(proxy_ips) >= 2:
            return proxy_ips[1]

    return None
