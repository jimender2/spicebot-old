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
This gains info about the current server
"""


# Start listener on welcome RPL, which should only ever be received once
@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_setup_server(bot, trigger):

    while not bot_startup_requirements_met(bot, ["botdict"]):
        pass

    # create temporary lists of servers on the SpiceNetwork
    bot.memory["botdict"]["tempvals"]["servers_list"] = dict()

    # create permanent lists of servers on the SpiceNetwork
    if "servers_list" not in bot.memory["botdict"].keys():
        bot.memory["botdict"]['servers_list'] = dict()

    bot.memory["botdict"]["tempvals"]['server'] = str(trigger.sender).lower()

    serverparts = str(trigger.sender).lower().split(".")
    servertld = serverparts[-1]
    del serverparts[-1]
    servername = serverparts[-1]
    if servername == 'spicebot':
        servername = 'SpiceBot'
    elif servername == 'freenode':
        servername = 'Freenode'
    else:
        servername = servername.title
    bot.memory["botdict"]["tempvals"]['servername'] = servername
    bot.memory["botdict"]["tempvals"]['server'] = str("irc." + servername + "." + servertld).lower()

    # Temp listing for server
    if str(trigger.sender).lower() not in bot.memory["botdict"]["tempvals"]["servers_list"].keys():
        bot.memory["botdict"]["tempvals"]["servers_list"][str(trigger.sender).lower()] = dict()

    # permanent listing of the server
    if str(trigger.sender).lower() not in bot.memory["botdict"]['servers_list'].keys():
        bot.memory["botdict"]['servers_list'][str(bot.memory["botdict"]["tempvals"]['server']).lower()] = dict()

    bot_startup_requirements_set(bot, "server")
