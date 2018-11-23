#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module

# imports for system and OS access, directories
import os
import sys
import socket
import threading

# imports based on THIS file
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


HOST = '127.0.0.1'
PORT = 7675  # SOPL
TARGET = '#spicebottest'

sock = None


def setup(bot):
    global sock
    if sock:  # the socket will already exist if the module is being reloaded
        return
    sock = socket.socket()  # the default socket types should be fine for sending text to localhost
    try:
        sock.bind((HOST, PORT))
    except socket.error as msg:
        print "socket fucked up: " + str(msg[0]) + ": " + msg[1]
        return
    sock.listen(5)


def shutdown(bot):
    global sock
    sock.close()
    sock = None  # best to be explicit about things


def receiver(conn, bot):
    buffer = ''
    while True:
        data = conn.recv(2048)
        buffer += data
        if not data:
            conn.close()
            break
        if '\n' in buffer:
            data, _, buffer = buffer.rpartition('\n')
            sayit(bot, data)
    sayit(bot, buffer)


def sayit(bot, data):
    for line in data.splitlines():
        bot.say("[sockmsg] %s" % line, TARGET)


# Start listener on welcome RPL, which should only ever be received once
@event('001')
@rule('.*')
def listener(bot, trigger):
    global sock
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=receiver, args=(conn, bot), name='sockmsg-listener').start()
