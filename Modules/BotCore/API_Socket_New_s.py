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

    beguinelisten = False
    while not beguinelisten:
        if "botdict_loaded" in bot.memory:
            beguinelisten = True
        else:
            time.sleep(1)
    bot.msg("#spicebottest", "[S] testing api")

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 9091)
    bot.msg("#spicebottest", "[S] starting up on " + str(server_address))
    sock.connect(server_address)

    try:
        # Send data
        message = 'This is the message.  It will be repeated.'
        bot.msg("#spicebottest", "[S] sending " + str(message))
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while True:
            data = sock.recv(2048)
            amount_received += len(data)
            bot.msg("#spicebottest", "[S] received " + str(data))

    finally:
        bot.msg("#spicebottest", "[S] closing socket")
        sock.close()
