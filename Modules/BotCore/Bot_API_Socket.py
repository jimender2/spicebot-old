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

    # response_headers
    response_headers = {
                        'Content-Type': 'text/html; encoding=utf8',
                        'Content-Length': len(msg),
                        'Connection': 'close',
                        }
    response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
    response_proto = 'HTTP/1.1'
    response_status = '200'
    response_status_text = 'OK'  # this can be random
    r = '%s %s %s\r\n' % (response_proto, response_status, response_status_text)

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
                        break

                    # Sending Botdict out
                    if spicemanip(bot, str(data), 1) == "GET":

                        # Possibly add a api key

                        # copy dict to not overwrite
                        savedict = copy.deepcopy(bot.memory["botdict"])

                        # don't include this
                        if "tempvals" in savedict:
                            if 'sock' in savedict["tempvals"]:
                                del savedict["tempvals"]['sock']

                        # convert to json
                        msg = json.dumps(savedict, default=json_util.default).encode('utf-8')

                        # sending all this stuff
                        try:
                            stderr("[API] Sending data back to the client.")
                            connection.send(r)
                            connection.send(response_headers_raw)
                            connection.send('\r\n')  # to separate headers from body
                            connection.send(msg.encode(encoding="utf-8"))
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
                            break

                        # make sure we have the correct format to respond with
                        if not isinstance(jsondict, dict):
                            stderr("[API] Recieved content not in correct dict format.")
                            break

                        # Possibly add a api key

                        # type
                        if "type" not in jsondict.keys():
                            stderr("[API] No type included.")
                            break

                        if jsondict["type"] == "message":

                            # must be a message included
                            if "message" not in jsondict.keys():
                                stderr("[API] No message included.")
                                break

                            # must be a channel or user included
                            if "channel" not in jsondict.keys():
                                stderr("[API] No channel included.")
                                break

                            # must be a current channel or user
                            if not bot_check_inlist(bot, jsondict["channel"], bot.memory["botdict"]["tempvals"]['channels_list'].keys()) and not bot_check_inlist(bot, jsondict["channel"], bot.memory["botdict"]["tempvals"]['all_current_users']):
                                stderr("[API] " + str(jsondict["channel"]) + " is not a current channel or user.")
                                break

                            # success
                            osd(bot, jsondict["channel"], 'say', jsondict["message"])
                            msg = str("[API] Success: Sendto=" + jsondict["channel"] + " message='" + str(jsondict["message"]) + "'")
                            stderr(msg)
                            connection.send(r)
                            connection.send(response_headers_raw)
                            connection.send('\r\n')  # to separate headers from body
                            connection.send(msg.encode(encoding="utf-8"))
                            break

                        else:
                            stderr("[API] Type does not exist")
                            break

                else:
                    break

        except Exception as e:
            stderr("[API] Error: (%s)" % (e))
            continue

        # If broken enough, connection will be closed
        finally:
            # Clean up the connection
            stderr("[API] Closing Connection.")
            connection.close()
