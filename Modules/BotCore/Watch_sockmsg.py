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


# Start listener on welcome RPL, which should only ever be received once
@event('001')
@rule('.*')
def listener(bot, trigger):

    beguineload = False
    while not beguineload:
        if "botdict_loaded" in bot.memory:
            beguineload = True
        else:
            time.sleep(1)

    beguinelisten = False
    while not beguinelisten:
        if bot.memory["botdict"]["tempvals"]['sock']:
            beguinelisten = True
        else:
            time.sleep(1)

    # Json API listner
    if bot.memory["botdict"]["tempvals"]['sock']:
        while True:
            conn, addr = bot.memory["botdict"]["tempvals"]['sock'].accept()
            threading.Thread(target=sock_receiver, args=(conn, bot), name='sockmsg-listener').start()
