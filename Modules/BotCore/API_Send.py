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
    return

    beguinelisten = False
    while not beguinelisten:
        if "botdict" in bot.memory:
            if bot.memory["botdict"]["tempvals"]['sock']:
                beguinelisten = True
            else:
                time.sleep(1)
        else:
            time.sleep(1)

    # Json API listner
    while True:
        conn, addr = bot.memory["botdict"]["tempvals"]['sock'].accept()
        print("Connection accepted from " + repr(addr[1]))

        conn.send("Server approved connection\n")
        print repr(addr[1]) + ": " + c.recv(1026)
        conn.close()


"""

# Json API listner
while True:
    conn, addr = bot.memory["botdict"]["tempvals"]['sock'].accept()
    threading.Thread(target=sock_receiver, args=(conn, bot), name='sockmsg-listener').start()

        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('0.0.0.0', bot.memory["botdict"]['sock_port']))
        clientsocket.send(bot.memory["botdict"])
"""
