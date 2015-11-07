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
