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
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


"""
This will pull files fropm Github and restart the bots service
"""


@nickname_commands('update')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "monologue"]):
        pass

    botcom = botcom_nick(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    if not bot_nickcom_run_check(bot, botcom):
        return osd(bot, botcom.instigator, 'notice', "I was unable to process this Bot Nick command due to privilege issues.")

    stderr("Recieved Command to update.")
    osd(bot, bot.privileges.keys(), 'say', "Received command from " + botcom.instigator + " to update from Github and restart. Be Back Soon!")

    # Directory Permissions
    os.system("sudo chown -R " + str(os_dict["user"]) + ":sudo /home/spicebot/.sopel/" + str(bot.nick) + "/")

    # Pull directory from github
    gitpull(bot, "/home/spicebot/.sopel/" + str(bot.nick))

    # close connection
    if 'sock' in bot.memory:
        if bot.memory['sock']:
            stderr("[API] Closing Connection.")
            bot.memory['sock'].close()

    # restart systemd service
    service_manip(bot, str(bot.nick), "restart")
