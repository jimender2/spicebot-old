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


# Start sender on welcome RPL, which should only ever be received once
@event('001')
@rule('.*')
@sopel.module.thread(True)
def api_socket_client(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "server", "channels", "users", "bot_api"]):
        pass

    bot_startup_requirements_set(bot, "bot_api_client")

    # If Connection Closes, this should reopen it forever
    # while True:
    #    hostsprocessor(bot)
    hostsprocessor(bot)


def hostsprocessor(bot):
    hostslist = hardcode_dict["bot_ip_addresses"]
    for host in hostslist:
        for i in range(8000, 8051):

            # don't process current bot
            if host != bot.memory["botdict"]["tempvals"]['networking']['ip_addresses'] and str(i) != str(bot.memory['sock_port']):

                try:
                    apiquery = bot_api_fetch(bot, i, host)
                except Exception as e:
                    apiquery = dict()

                if apiquery != {}:
                    bot.msg("#spicebottest", str(host) + ":" + str(i))

                    if "tempvals" not in apiquery.keys():
                        pass

                    if "bot_info" in apiquery["tempvals"].keys():
                        querytest = str(apiquery["tempvals"]["bot_info"].keys())
                        bot.msg("#spicebottest", querytest)
