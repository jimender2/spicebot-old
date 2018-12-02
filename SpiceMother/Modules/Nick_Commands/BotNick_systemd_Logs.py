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


@nickname_commands('update')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    osd(bot, botcom.channel_current, 'action', "Is Examining systemd Log(s).")

    debuglines = []
    ignorearray = ["COMMAND=/usr/sbin/service", "pam_unix(sudo:session)", "COMMAND=/bin/chown", "Docs: http://sopel.chat/", "Main PID:", "systemctl status", "sudo service"]
    for line in os.popen("sudo service " + str(bot.nick) + " status").read().split('\n'):
        if not any(x in str(line) for x in ignorearray):
            debuglines.append(str(line))

    if len(debuglines) == 0:
        return osd(bot, botcom.channel_current, 'say', spicemanip(bot, nobotlogs, 'andlist') + " had no log(s) for some reason")

    for line in debuglines:
        osd(bot, botcom.channel_current, 'say', line)
