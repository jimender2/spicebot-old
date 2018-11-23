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

    host = '0.0.0.0'
    port = 8000

    # Client code:
    client = Client()
    client.connect(host, port).send({'some_list': [123, 456]})
    response = client.recv()
    # response now is {'data': {'some_list': [123, 456]}}
    client.close()

    # Server code:
    server = Server(host, port)
    server.accept()
    data = server.recv()
    # data now is: {'some_list': [123, 456]}
    server.send({'data': data}).close()


"""

    beguinelisten = False
    while not beguinelisten:
        if "botdict_loaded" in bot.memory:
            beguinelisten = True
        else:
            time.sleep(1)

    # API listner
    while True:
        conn, addr = bot.memory["botdict"]["tempvals"]['sock'].accept()
        threading.Thread(target=bot_api_socket_handler, args=(conn, bot), name='sockmsg-listener').start()
"""
