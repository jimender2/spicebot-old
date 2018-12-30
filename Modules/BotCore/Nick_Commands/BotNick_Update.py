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


comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "",
            'privs': ['admin', 'OP'],
            "example": "",
            "exampleresponse": "",
            }


"""
This will pull files fropm Github and restart the bots service
"""


@nickname_commands('update')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    botcom = botcom_nick(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    # does not apply to bots
    if "altbots" in bot.memory:
        if bot_check_inlist(bot, botcom.instigator, bot.memory["altbots"].keys()):
            return

    if not bot_permissions_check(bot, botcom):
        return osd(bot, botcom.instigator, 'notice', "I was unable to process this Bot Nick command due to privilege issues.")

    if 'sock_port' in bot.memory:
        if bot.memory['sock_port']:
            bot_api_send_self_command(bot, botcom, "update")
            return

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

    stderr("Saving Botdict.")
    botdict_save(bot)

    # restart systemd service
    service_manip(bot, str(bot.nick), "restart")
