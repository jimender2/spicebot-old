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
        if "botdict" in bot.memory:
            beguinelisten = True
        else:
            time.sleep(1)

    server = bot.memory["botdict"]["tempvals"]['sock']
    server.setblocking(0)
    inputs = [server]
    outputs = []
    message_queues = {}

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = Queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                outputs.remove(s)
            else:
                s.send(next_msg)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]


"""


    # API listner
    while True:
        conn, addr = bot.memory["botdict"]["tempvals"]['sock'].accept()
        threading.Thread(target=bot_api_socket_handler, args=(conn, bot), name='sockmsg-listener').start()


def bot_api_socket_handler(conn, bot):
    data = conn.recv(2048)
    if not data:
        conn.close()
    else:

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
"""
