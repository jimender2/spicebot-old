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
    bot.memory['sock'] = None
    currenthost_ip = socket.gethostbyname(socket.gethostname())
    previouslyusedport = get_database_value(bot, bot.nick, 'sock_port') or None
    if not bot.memory['sock'] or not previouslyusedport:
        bot.memory['sock'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # port number to use, try previous port, if able
        currentport = None
        if previouslyusedport:
            if not is_port_in_use(previouslyusedport):
                currentport = previouslyusedport
        if not currentport:
            currentport = find_unused_port_in_range(bot, 8080, 9090)
        set_database_value(bot, bot.nick, 'sock_port', currentport)
        try:
            bot.memory['sock'].bind(('0.0.0.0', previouslyusedport))
            stderr("Loaded socket on port %s" % (previouslyusedport))
            bot.memory['sock'].listen(10)
        except socket.error as msg:
            stderr("Error loading socket on port %s: %s (%s)" % (previouslyusedport, str(msg[0]), str(msg[1])))
            return
    sock = bot.memory['sock']

    # register this port with the other bots
    botslist = []
    for bots in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        if bots != str(bot.nick):
            if bot.memory["botdict"]["tempvals"]['bots_list'][bots]['directory']:
                botslist.append(bots)
                registerdict = {"bot": str(bot.nick), "host": str(currenthost_ip), "port": str(bot.memory["botdict"]['sock_port'])}
                msg = json.dumps(registerdict, default=json_util.default).encode('utf-8')
                bot.msg(bots, msg)
    if botslist != []:
        stderr("Sent API registration to " + str(spicemanip(bot, botslist, 'andlist')))

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
                        response_headers_raw, r = bot_api_response_headers(bot, msg)

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

                        if "sender" not in jsondict.keys():
                            sender = "API"
                        else:
                            sender = jsondict["sender"]

                        # message a specific channel/user or all channels
                        if jsondict["type"] == "message":

                            # must be a message included
                            if "message" not in jsondict.keys():
                                stderr("[API] No message included.")
                                break

                            # must be a channel or user included
                            if "targets" not in jsondict.keys():
                                stderr("[API] No targets included.")
                                break

                            # accept list inputs
                            if not isinstance(jsondict["targets"], list):
                                listtargets = [jsondict["targets"]]
                            else:
                                listtargets = jsondict["targets"]

                            # check all targets in list
                            failedtargets = []
                            goodtargets = []
                            for target in listtargets:
                                if not bot_check_inlist(bot, target, bot.memory["botdict"]["tempvals"]['channels_list'].keys()) and not bot_check_inlist(bot, target, bot.memory["botdict"]["tempvals"]['all_current_users']) and target not in ["all_chan", "all_user"]:
                                    failedtargets.append(target)
                                else:
                                    goodtargets.append(target)

                            if failedtargets != []:
                                stderr("[API] " + str(spicemanip(bot, failedtargets, 'andlist')) + " is/are not current channel(s) or user(s).")

                            if goodtargets == []:
                                stderr("[API] No current channel or user to target.")
                                break

                            for target in goodtargets:

                                if target in ["all_chan", "all_user"]:
                                    if target == "all_chan":
                                        targets = bot.memory["botdict"]["tempvals"]['channels_list'].keys()
                                    if target == "all_user":
                                        targets = bot.memory["botdict"]["tempvals"]['all_current_users']
                                else:
                                    targets = [target]

                                osd(bot, targets, 'say', jsondict["message"])
                            # success
                            stderr("[API] Success: Sendto=" + str(jsondict["targets"]) + " message='" + str(jsondict["message"]) + "'")
                            break

                        elif jsondict["type"] == "command":

                            # must be a message included
                            if "command" not in jsondict.keys():
                                stderr("[API] No command included.")
                                break

                            if jsondict["command"] == 'update':
                                stderr("[API] Recieved Command to update.")
                                for channel in bot.channels:
                                    if sender != "API":
                                        osd(bot, channel, 'say', "Recived API command from " + sender + " to update from Github and restart. Be Back Soon!")
                                    else:
                                        osd(bot, channel, 'say', "Recived API command to update from Github and restart. Be Back Soon!")

                                # Pull directory from github
                                stderr("[API] Pulling From Github.")
                                g = git.cmd.Git(bot.memory["botdict"]["tempvals"]['bots_list'][str(bot.nick)]['directory'])
                                g.pull()

                                # close connection
                                stderr("[API] Closing Connection.")
                                connection.close()

                                # restart systemd service
                                stderr("[API] Restarting Service.")
                                os.system("sudo service " + str(bot.nick) + " restart")

                                # Pointless, but breaks the loop if needbe
                                break

                            elif jsondict["command"] == 'restart':
                                stderr("[API] Recieved Command to restart.")
                                for channel in bot.channels:
                                    if sender != "API":
                                        osd(bot, channel, 'say', "Recived API command from " + sender + " to restart. Be Back Soon!")
                                    else:
                                        osd(bot, channel, 'say', "Recived API command to restart. Be Back Soon!")

                                # close connection
                                stderr("[API] Closing Connection.")
                                connection.close()

                                # restart systemd service
                                stderr("[API] Restarting Service.")
                                os.system("sudo service " + str(bot.nick) + " restart")

                                # Pointless, but breaks the loop if needbe
                                break

                            else:
                                stderr("[API] Included Command invalid.")
                                break

                        else:
                            stderr("[API] Included Type invalid.")
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
