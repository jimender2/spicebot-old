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
                stderr("[API] Received data.")
                if data:

                    # verify bot is reasdy to recieve a message
                    if "botdict_loaded" not in bot.memory:
                        stderr("[API] Not ready to process requests.")
                        return

                    # Sending Botdict out
                    if str(data).startswith("GET"):

                        # Possibly add a api key

                        # convert dict to string
                        # data_string = str(savedict)

                        # copy dict to not overwrite
                        savedict = bot.memory["botdict"].copy()

                        # don't include this
                        del savedict["tempvals"]['sock']

                        # convert to json
                        data_string = json.dumps(savedict, default=json_util.default).encode('utf-8')

                        try:
                            stderr("[API] Sending data back to the client.")
                            connection.sendall(data_string)
                            break
                        except Exception as e:
                            stderr("[API] Error Sending Data: (%s)" % (e))
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

        except Exception as e:
            stderr("[API] Error: (%s)" % (e))
            break

        finally:
            # Clean up the connection
            stderr("[API] Closing Connection.")
            connection.close()


class CustomEncoder(json.JSONEncoder):

    def default(self, o):

        if isinstance(o, datetime):
            return {'__datetime__': o.replace(microsecond=0).isoformat()}

        return {'__{}__'.format(o.__class__.__name__): o.__dict__}
