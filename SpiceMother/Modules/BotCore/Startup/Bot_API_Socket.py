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
@sopel.module.thread(True)
def api_socket_hub(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "server", "channels", "users"]):
        pass

    # Create a TCP/IP socket
    bot.memory['sock'] = None
    bot.memory['sock_port'] = get_database_value(bot, bot.nick, 'sock_port') or None
    if bot.memory['sock_port'] or bot.memory['sock_port'] == 'None':
        bot.memory['sock_port'] = int(bot.memory['sock_port'])
    if not bot.memory['sock'] or not bot.memory['sock_port']:
        bot.memory['sock'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # port number to use, try previous port, if able
        currentport = None
        if bot.memory['sock_port']:
            if not is_port_in_use(bot.memory['sock_port'], "0.0.0.0"):
                currentport = bot.memory['sock_port']
        if not currentport:
            currentport = find_unused_port_in_range(bot, 8000, 8050, "0.0.0.0")
        set_database_value(bot, bot.nick, 'sock_port', currentport)
        try:
            bot.memory['sock'].bind(('0.0.0.0', int(currentport)))
            stderr("Loaded socket on port %s" % (currentport))
            bot.memory['sock'].listen(10)
        except socket.error as msg:
            stderr("Error loading socket on port %s: %s (%s)" % (currentport, str(msg[0]), str(msg[1])))
            bot.memory['sock_port'] = None
            bot_startup_requirements_set(bot, "bot_api")
            return
    sock = bot.memory['sock']

    if "sock_dict" not in bot.memory:
        bot.memory["sock_dict"] = dict()
    if "sock_bot_list" not in bot.memory:
        bot.memory["sock_bot_list"] = []

    bot_startup_requirements_set(bot, "bot_api")

    # If Connection Closes, this should reopen it forever
    while True:
        api_socket_run(bot, sock)


def api_socket_run(bot, sock):

    while True:

        # Wait for a connection
        bot_logging(bot, "API", "[API] Waiting for a connection.")
        connection, client_address = sock.accept()

        try:
            bot_logging(bot, "API", "[API] Connection from " + str(client_address))

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(2048)
                bot_logging(bot, "API", "[API] Received data.")
                if data:

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
                            bot_logging(bot, "API", "[API] Sending data back to the client.")
                            connection.send(r)
                            connection.send(response_headers_raw)
                            connection.send('\r\n')  # to separate headers from body
                            connection.send(msg.encode(encoding="utf-8"))
                            break
                        except Exception as e:
                            bot_logging(bot, "API", "[API] Error Sending Data: (%s)" % (e))
                            break

                    else:

                        # catch errors with api format
                        try:
                            jsondict = eval(data)
                        except Exception as e:
                            bot_logging(bot, "API", "[API] Error recieving: (%s)" % (e))
                            break

                        # make sure we have the correct format to respond with
                        if not isinstance(jsondict, dict):
                            bot_logging(bot, "API", "[API] Recieved content not in correct dict format.")
                            break

                        # Possibly add a api key

                        # type
                        if "type" not in jsondict.keys():
                            bot_logging(bot, "API", "[API] No type included.")
                            break

                        if "sender" not in jsondict.keys():
                            sender = "API"
                        else:
                            sender = jsondict["sender"]

                        # message a specific channel/user or all channels
                        if jsondict["type"] == "message":

                            # must be a message included
                            if "message" not in jsondict.keys():
                                bot_logging(bot, "API", "[API] No message included.")
                                break

                            # must be a channel or user included
                            if "targets" not in jsondict.keys():
                                bot_logging(bot, "API", "[API] No targets included.")
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
                                if not bot_check_inlist(bot, target, bot.memory["botdict"]["tempvals"][str(bot.memory["botdict"]["tempvals"]['server'])]['channels_list'].keys()) and not bot_check_inlist(bot, target, bot.memory["botdict"]["tempvals"][str(bot.memory["botdict"]["tempvals"]['server'])]['all_current_users']) and target not in ["all_chan", "all_user"]:
                                    failedtargets.append(target)
                                else:
                                    goodtargets.append(target)

                            if failedtargets != []:
                                bot_logging(bot, "API", "[API] " + str(spicemanip(bot, failedtargets, 'andlist')) + " is/are not current channel(s) or user(s).")

                            if goodtargets == []:
                                bot_logging(bot, "API", "[API] No current channel or user to target.")
                                break

                            for target in goodtargets:

                                if target in ["all_chan", "all_user"]:
                                    if target == "all_chan":
                                        targets = bot.memory["botdict"]["tempvals"][str(bot.memory["botdict"]["tempvals"]['server'])]['channels_list'].keys()
                                    if target == "all_user":
                                        targets = bot.memory["botdict"]["tempvals"][str(bot.memory["botdict"]["tempvals"]['server'])]['all_current_users']
                                else:
                                    targets = [target]

                                osd(bot, targets, 'say', jsondict["message"])
                            # success
                            bot_logging(bot, "API", "[API] Success: Sendto=" + str(jsondict["targets"]) + " message='" + str(jsondict["message"]) + "'")
                            break

                        elif jsondict["type"] == "command":

                            # must be a message included
                            if "command" not in jsondict.keys():
                                bot_logging(bot, "API", "[API] No command included.")
                                break

                            if jsondict["command"] == 'update':
                                stderr("[API] Recieved Command to update.")
                                for channel in bot.channels:
                                    if sender != "API":
                                        osd(bot, channel, 'say', "Recived API command from " + sender + " to update from Github and restart. Be Back Soon!")
                                    else:
                                        osd(bot, channel, 'say', "Recived API command to update from Github and restart. Be Back Soon!")

                                # Directory Permissions
                                os.system("sudo chown -R " + str(os_dict["user"]) + ":sudo /home/spicebot/.sopel/" + str(bot.nick) + "/")

                                # Pull directory from github
                                gitpull(bot, "/home/spicebot/.sopel/" + str(bot.nick))

                                # close connection
                                stderr("[API] Closing Connection.")
                                connection.close()

                                # restart systemd service
                                service_manip(bot, str(bot.nick), "restart")

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
                                service_manip(bot, str(bot.nick), "restart")

                                # Pointless, but breaks the loop if needbe
                                break

                            else:
                                bot_logging(bot, "API", "[API] Included Command invalid.")
                                break

                        else:
                            bot_logging(bot, "API", "[API] Included Type invalid.")
                            break

                else:
                    break

        except Exception as e:
            bot_logging(bot, "API", "[API] Error: (%s)" % (e))
            continue

        # If broken enough, connection will be closed
        finally:
            # Clean up the connection
            bot_logging(bot, "API", "[API] Closing Connection.")
            connection.close()
