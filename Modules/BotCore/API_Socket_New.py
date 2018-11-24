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
    bot.msg("#spicebottest", "testing api")

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 10000)
    bot.msg("#spicebottest", "starting up on " + str(server_address))
    sock.bind(server_address)
    sock.connect(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        bot.msg("#spicebottest", "waiting for a connection")
        connection, client_address = sock.accept()

        bot.msg("#spicebottest", "connection from " + str(client_address))

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(2048)
            bot.msg("#spicebottest", "'received " + str(data))
            if data:
                bot.msg("#spicebottest", "sending data back to the client")
                connection.sendall(data)
            else:
                bot.msg("#spicebottest", "no more data from " + str(client_address))
                break
