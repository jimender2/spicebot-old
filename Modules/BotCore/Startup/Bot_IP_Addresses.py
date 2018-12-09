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


# Start listener on welcome RPL, which should only ever be received once
@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_ip_addr(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict"]):
        pass

    bot.memory["botdict"]["tempvals"]['networking'] = dict()

    bot.memory["botdict"]["tempvals"]['networking']['interfaces'] = netifaces.interfaces()

    bot.memory["botdict"]["tempvals"]['networking']['ip_addresses'] = []

    for i in bot.memory["botdict"]["tempvals"]['networking']['interfaces']:
        if i == 'lo':
            continue
        iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
        if iface:
            for j in iface:
                bot.memory["botdict"]["tempvals"]['networking']['ip_addresses'].append(str(j['addr']))

    bot_startup_requirements_set(bot, "ip_address")
