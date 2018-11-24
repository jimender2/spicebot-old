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
    bot.msg("#spicebottest", "[R] testing api")

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('', 9091)
    bot.msg("#spicebottest", "[R] starting up on " + str(sock.getsockname()))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(10)

    while True:
        # Wait for a connection
        bot.msg("#spicebottest", "[R] waiting for a connection")
        connection, client_address = sock.accept()

        try:
            bot.msg("#spicebottest", "[R] connection from " + str(client_address))

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(2048)
                bot.msg("#spicebottest", "[R] received " + str(data))
                if data:
                    bot.msg("#spicebottest", "[R] sending data back to the client")
                    connection.sendall(data)

                    # verify bot is reasdy to recieve a message
                    if "botdict_loaded" not in bot.memory:
                        stderr("[API] Not ready to process requests.")
                        return

                    # catch errors with api format
                    try:
                        jsondict = eval(data)
                    except Exception as e:
                        stderr("[API] Error recieving: (%s)" % (e))
                        return

                    # must be a message included
                    if not jsondict["message"]:
                        stderr("[API] No message included.")
                        return

                    # must be a channel or user included
                    if not jsondict["channel"]:
                        stderr("[API] No channel included.")
                        return

                    # must be a current channel or user
                    if not bot_check_inlist(bot, jsondict["channel"], bot.memory["botdict"]["tempvals"]['channels_list'].keys()) and not bot_check_inlist(bot, jsondict["channel"], bot.memory["botdict"]["tempvals"]['all_current_users']):
                        stderr("[API] " + str(jsondict["channel"]) + " is not a current channel or user.")
                        return

                    # Possibly add a api key

                    # success
                    stderr("[API] Success: Sendto=" + jsondict["channel"] + " message='" + str(jsondict["message"]) + "'")
                    osd(bot, jsondict["channel"], 'say', jsondict["message"])

                else:
                    bot.msg("#spicebottest", "[R] no more data from " + str(client_address))
                    break

        finally:
            # Clean up the connection
            bot.msg("#spicebottest", "[R] closing connection")
            connection.close()
