# -*- include: utf-8 -*-

from subprocess import Popen, PIPE


def cmd(*args):
    """Execute a shell command"""

    return Popen(args, stdout=PIPE, stderr=PIPE).communicate()[0]
