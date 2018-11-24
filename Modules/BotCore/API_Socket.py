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

    # Create a TCP/IP socket
    if not bot.memory["botdict"]["tempvals"]['sock'] or not bot.memory["botdict"]['sock_port']:
        bot.memory["botdict"]["tempvals"]['sock'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # port number to use, try previous port, if able
        currentport = None
        if bot.memory["botdict"]['sock_port']:
            if not is_port_in_use(bot.memory["botdict"]['sock_port']):
                currentport = bot.memory["botdict"]['sock_port']
        if not currentport:
            currentport = find_unused_port_in_range(bot, 8080, 9090)
        bot.memory["botdict"]['sock_port'] = currentport
        try:
            bot.memory["botdict"]["tempvals"]['sock'].bind(('0.0.0.0', bot.memory["botdict"]['sock_port']))
            stderr("Loaded socket on port %s" % (bot.memory["botdict"]['sock_port']))
            bot.memory["botdict"]["tempvals"]['sock'].listen(10)
        except socket.error as msg:
            stderr("Error loading socket on port %s: %s (%s)" % (bot.memory["botdict"]['sock_port'], str(msg[0]), str(msg[1])))
            return
    sock = bot.memory["botdict"]["tempvals"]['sock']

    while True:
        # Wait for a connection
        stderr("[API] Waiting for a connection.")
        connection, client_address = sock.accept()

        try:
            stderr("[API] Connection from " + str(client_address))

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(2048)
                stderr("[API] received " + str(data))
                if data:

                    # verify bot is reasdy to recieve a message
                    if "botdict_loaded" not in bot.memory:
                        stderr("[API] Not ready to process requests.")
                        return

                    # Sending Botdict out
                    if str(data).startswith("GET"):

                        # Possibly add a api key

                        stderr("[API] sending data back to the client " + str(data))
                        connection.sendall(str(str(bot.memory["botdict"]) + "\n"))
                        break

                    else:

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
                        break

                else:
                    break

        # finally:
            # Clean up the connection
        #    stderr("[API] Closing Connection.")
        #    connection.close()
