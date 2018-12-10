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
    hostsprocess = []
    for host in hostslist:
        for i in range(8000, 8051):

            # don't process current bot
            if host in bot.memory["botdict"]["tempvals"]['networking']['ip_addresses'] and str(i) == str(bot.memory['sock_port']):
                donothing = True
            else:

                if bot_api_port_test(bot, host, i):
                    hostdict = {"host": host, "port": i}
                    hostsprocess.append(hostdict)

    # this is where we will process the info from the other bots
    for hostdict in hostsprocess:
        try:
            apiquery = bot_api_fetch(bot, hostdict["port"], hostdict["host"])
        except Exception as e:
            apiquery = dict()

        if apiquery != {}:

            if "tempvals" in apiquery.keys():

                if "bot_info" in apiquery["tempvals"].keys():
                    querytest = str(apiquery["tempvals"]["bot_info"].keys())

            """
            if "users" in apiquery.keys():

                for user in apiquery["users"]:
                    if user not in bot.memory["botdict"]["users"]:
                        bot.memory["botdict"]["users"][user] = dict()

                    for sortingkey in apiquery["users"][user].keys():
                        if sortingkey not in bot.memory["botdict"]["users"][user].keys():
                            bot.memory["botdict"]["users"][user][sortingkey] = dict()

                        for usekey in apiquery["users"][user][sortingkey].keys():
                            if usekey not in bot.memory["botdict"]["users"][user][sortingkey].keys():
                                bot.memory["botdict"]["users"][user][sortingkey][usekey] = dict()

                            if not isinstance(bot.memory["botdict"]["users"][nick][sortingkey][usekey], dict):
                                oldvalue = bot.memory["botdict"]["users"][nick][sortingkey][usekey]
                                bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
                                bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = oldvalue

                            if "value" not in bot.memory["botdict"]["users"][user][sortingkey][usekey].keys():
                                bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = None
                            if "timestamp" not in bot.memory["botdict"]["users"][nick][sortingkey][usekey].keys():
                                bot.memory["botdict"]["users"][nick][sortingkey][usekey]["timestamp"] = 0

                            if not isinstance(apiquery["users"][user][sortingkey][usekey], dict):
                                oldapivalue = apiquery["users"][user][sortingkey][usekey]
                                apiquery["users"][user][sortingkey][usekey]["value"] = oldapivalue
                                apiquery["users"][user][sortingkey][usekey]["timestamp"] = 0

                            if apiquery["users"][user][sortingkey][usekey]["timestamp"] > bot.memory["botdict"]["users"][nick][sortingkey][usekey]["timestamp"]:
                                set_nick_value(bot, user, "long", sortingkey, usekey, apiquery["users"][user][sortingkey][usekey]["value"])
                                """
