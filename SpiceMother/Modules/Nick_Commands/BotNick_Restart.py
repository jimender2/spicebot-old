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


@nickname_commands('restart')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    stderr("Recieved Command to update.")
    osd(bot, bot.privileges.keys(), 'say', "Received command from " + trigger.nick + " to restart systemd service. Be Back Soon!")

    # close connection
    # stderr("[API] Closing Connection.")
    # connection.close()

    # restart systemd service
    stderr("Restarting Service.")
    os.system("sudo service " + str(bot.nick) + " restart")
