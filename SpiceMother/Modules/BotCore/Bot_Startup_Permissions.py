#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module

# imports for system and OS access, directories
import os
import sys

# imports based on THIS file
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_main(bot, trigger):

    # os.system("sudo chown -R spicebot:sudo /home/spicebot/.sopel/")
    chown("/home/spicebot/.sopel/" + str(bot.nick) + "/", "spicebot", "sudo")


def chown(path, user=None, group=None):
    """Change owner user and group of the given path.

    user and group can be the uid/gid or the user/group names, and in that case,
    they are converted to their respective uid/gid.
    """

    if user is None and group is None:
        raise ValueError("user and/or group must be set")

    _user = user
    _group = group

    # -1 means don't change it
    if user is None:
        _user = -1
    # user can either be an int (the uid) or a string (the system username)
    elif isinstance(user, basestring):
        _user = os.popen("id -u %s" % user).read().strip()
        if _user is None:
            raise LookupError("no such user: {!r}".format(user))

    if group is None:
        _group = -1
    elif not isinstance(group, int):
        _group = os.popen("id -g %s" % group).read().strip()
        if _group is None:
            raise LookupError("no such group: {!r}".format(group))

    os.chown(path, _user, _group)
