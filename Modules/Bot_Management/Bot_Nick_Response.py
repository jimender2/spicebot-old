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

# valid commands that the bot will reply to by name
valid_botnick_commands = {
                            "uptime": {
                                        'privs': [],
                                        },
                            "canyouseeme": {
                                        'privs': [],
                                        },
                            "gender": {
                                        'privs': [],
                                        },
                            "owner": {
                                        'privs': [],
                                        },
                            "admins": {
                                        'privs': [],
                                        },
                            "channel": {
                                        'privs': [],
                                        },
                            "msg": {
                                    'privs': ['admin', 'OP'],
                                    },
                            "action": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "notice": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "debug": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "update": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "restart": {
                                        'privs': ['admin', 'OP'],
                                        },
                            }


"""
bot.nick do this
"""

# TODO make sure restart and update save database


@nickname_commands('(.*)')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):
    if "botdict_loaded" not in bot.memory:
        osd(bot, trigger.nick, 'notice', "Please wait while I load my dictionary configuration.")
        return

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # valid commands
    global valid_botnick_commands

    # instigator
    botcom.instigator = trigger.nick

    # channel
    botcom.channel_current = trigger.sender

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, '2+', 'list')

    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    invalidcomslist = []
    for command_split_partial in commands_array:
        botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')

        # Command Used
        botcom.command_main = spicemanip(bot, botcom.triggerargsarray, 1)
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

        if botcom.command_main.lower() in valid_botnick_commands.keys():

            if bot_command_run_check(bot, botcom):

                bot_command_function_run = str('bot_command_function_' + botcom.command_main.lower() + '(bot, botcom)')
                eval(bot_command_function_run)
            else:
                invalidcomslist.append(botcom.command_main)

    # Display Invalids coms used
    if invalidcomslist != []:
        osd(bot, botcom.instigator, 'notice', "I was unable to process the following Bot Nick commands due to privilege issues: " + spicemanip(bot, invalidcomslist, 'andlist'))


def bot_command_run_check(bot, botcom):
    global valid_botnick_commands
    commandrun = True

    if 'privs' in valid_botnick_commands[botcom.command_main.lower()].keys():
        commandrunconsensus = []

        if 'admin' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bot_admins']:
                commandrunconsensus.append('False')
            else:
                commandrunconsensus.append('True')

        if 'OP' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if botcom.channel_current.startswith('#'):
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanops']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if 'HOP' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if botcom.channel_current.startswith('#'):
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanhalfops']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if 'VOICE' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if botcom.channel_current.startswith('#'):
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanvoices']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if valid_botnick_commands[botcom.command_main.lower()]['privs'] == []:
            commandrunconsensus.append('True')

        if 'True' not in commandrunconsensus:
            commandrun = False

    return commandrun


"""
Basic Running Operations
"""


def bot_command_function_update(bot, botcom):

    targetbots = []
    if botcom.triggerargsarray == []:
        targetbots.append(bot.nick)
    elif 'all' in botcom.triggerargsarray:
        for targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            targetbots.append(targetbot)
    else:
        for targetbot in botcom.triggerargsarray:
            if targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                targetbots.append(targetbot)

    # current bot should be last
    if str(bot.nick) in targetbots:
        targetbots.remove(str(bot.nick))
        targetbots.append(str(bot.nick))

    if targetbots == []:
        osd(bot, botcom.instigator, 'notice', "You have selected no bots to update.")
        return

    cannotproceed = []
    botcount = len(targetbots)

    if botcount == 1 and targetbots[0] == str(bot.nick):
        if targetbots[0] in bot.memory["botdict"]["static"]['bots']["update_text"].keys():
            osd(bot, botcom.channel_current, 'say', bot.memory["botdict"]["static"]['bots']["update_text"][targetbots[0]].replace("$instigator", botcom.instigator))
        else:
            osd(bot, botcom.channel_current, 'say', botcom.instigator + " commanded me to update from Github and restart. Be Back Soon!")
    else:
        osd(bot, [botcom.channel_current], 'say', botcom.instigator + " commanded me to update " + spicemanip(bot, targetbots, 'andlist') + " from Github and restart.")

    for targetbot in targetbots:

        if bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['directory']:

            osd(bot, botcom.channel_current, 'action', "Is Pulling " + str(bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['directory']) + " From Github...")
            bot_update(bot, targetbot)

            osd(bot, botcom.channel_current, 'action', "Is Restarting the " + targetbot + " Service...")
            bot_restart(bot, targetbot)

            botcount -= 1
            if botcount > 0:
                osd(bot, botcom.channel_current, 'say', "     ")

        else:
            cannotproceed.append(targetbot)

    if cannotproceed != []:
        osd(bot, botcom.channel_current, 'say', spicemanip(bot, cannotproceed, 'andlist') + " could not be updated.")


def bot_command_function_restart(bot, botcom):

    targetbots = []
    if botcom.triggerargsarray == []:
        targetbots.append(bot.nick)
    elif 'all' in botcom.triggerargsarray:
        for targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            targetbots.append(targetbot)
    else:
        for targetbot in botcom.triggerargsarray:
            if targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                targetbots.append(targetbot)

    # current bot should be last
    if str(bot.nick) in targetbots:
        targetbots.remove(str(bot.nick))
        targetbots.append(str(bot.nick))

    if targetbots == []:
        osd(bot, botcom.instigator, 'notice', "You have selected no bots to restart.")
        return

    cannotproceed = []
    botcount = len(targetbots)
    if botcount == 1 and targetbots[0] == str(bot.nick):
        if targetbots[0] in bot.memory["botdict"]["static"]['bots']["restart_text"].keys():
            osd(bot, botcom.channel_current, 'say', bot.memory["botdict"]["static"]['bots']["restart_text"][targetbots[0]].replace("$instigator", botcom.instigator))
        else:
            osd(bot, botcom.channel_current, 'say', botcom.instigator + " commanded me to restart. Be Back Soon!")
    else:
        osd(bot, [botcom.channel_current], 'say', botcom.instigator + " commanded me to restart " + spicemanip(bot, targetbots, 'andlist'))

    for targetbot in targetbots:

        if bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['directory']:

            osd(bot, botcom.channel_current, 'action', "Is Restarting the " + targetbot + " Service...")
            bot_restart(bot, targetbot)

            botcount -= 1
            if botcount > 0:
                osd(bot, botcom.channel_current, 'say', "     ")

        else:
            cannotproceed.append(targetbot)

    if cannotproceed != []:
        osd(bot, botcom.channel_current, 'say', spicemanip(bot, cannotproceed, 'andlist') + " could not be restarted.")


def bot_command_function_debug(bot, botcom):

    targetbots = {}
    if botcom.triggerargsarray == []:
        targetbots[str(bot.nick)] = dict()
    elif 'all' in botcom.triggerargsarray:
        for targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            targetbots[targetbot] = dict()
    else:
        for targetbot in botcom.triggerargsarray:
            if targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                targetbots[targetbot] = dict()

    osd(bot, botcom.channel_current, 'action', "Is Examining Log(s) for " + spicemanip(bot, targetbots.keys(), 'andlist'))

    for targetbot in targetbots.keys():

        debuglines = []
        ignorearray = ["COMMAND=/usr/sbin/service", "pam_unix(sudo:session)", "COMMAND=/bin/chown", "Docs: http://sopel.chat/", "Main PID:", "systemctl status", "sudo service"]
        for line in os.popen("sudo service " + targetbot + " status").read().split('\n'):
            if not any(x in str(line) for x in ignorearray):
                debuglines.append(str(line))

        targetbots[targetbot]['debuglines'] = debuglines

    botcount = len(targetbots.keys())
    nobotlogs = []
    for targetbot in targetbots.keys():
        if targetbots[targetbot]['debuglines'] != []:
            for line in targetbots[targetbot]['debuglines']:
                osd(bot, botcom.channel_current, 'say', line)
            botcount -= 1
            if botcount > 0:
                osd(bot, botcom.channel_current, 'say', "     ")
        else:
            nobotlogs.append(targetbot)

    if nobotlogs != []:
        osd(bot, botcom.channel_current, 'say', spicemanip(bot, nobotlogs, 'andlist') + " had no log(s) for some reason")


"""
Messaging channels
"""


def bot_command_function_msg(bot, botcom):

    # Channel
    targetchannels = []
    targetword = spicemanip(bot, botcom.triggerargsarray, 1)
    if targetword not in bot.memory["botdict"]["tempvals"]['channels_list'].keys() and targetword != 'all':
        if botcom.channel_current.startswith('#'):
            targetchannels.append(botcom.channel_current)
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    elif targetword == 'all':
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
        for targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
            targetchannels.append(targetchan)
    else:
        for targetchan in botcom.triggerargsarray:
            if targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
                targetchannels.append(targetchan)

    for channeltarget in targetchannels:
        if channeltarget in botcom.triggerargsarray:
            botcom.triggerargsarray.remove(channeltarget)

    botmessage = spicemanip(bot, botcom.triggerargsarray, 0)
    if not botmessage:
        osd(bot, botcom.instigator, 'notice', "You must specify a message.")
        return

    osd(bot, targetchannels, 'say', botmessage)


def bot_command_function_action(bot, botcom):

    # Channel
    targetchannels = []
    targetword = spicemanip(bot, botcom.triggerargsarray, 1)
    if targetword not in bot.memory["botdict"]["tempvals"]['channels_list'].keys() and targetword != 'all':
        if botcom.channel_current.startswith('#'):
            targetchannels.append(botcom.channel_current)
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    elif targetword == 'all':
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
        for targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
            targetchannels.append(targetchan)
    else:
        for targetchan in botcom.triggerargsarray:
            if targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
                targetchannels.append(targetchan)

    for channeltarget in targetchannels:
        if channeltarget in botcom.triggerargsarray:
            botcom.triggerargsarray.remove(channeltarget)

    botmessage = spicemanip(bot, botcom.triggerargsarray, 0)
    if not botmessage:
        osd(bot, botcom.instigator, 'notice', "You must specify a message.")
        return

    osd(bot, targetchannels, 'action', botmessage)


def bot_command_function_notice(bot, botcom):

    # Target
    targets = []
    targetword = spicemanip(bot, botcom.triggerargsarray, 1)
    if targetword not in bot.memory["botdict"]["tempvals"]['all_current_users'] and targetword != 'all':
        if botcom.channel_current.startswith('#'):
            targets.append(botcom.channel_current)
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid target.")
            return
    elif targetword == 'all':
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
        for target in bot.memory["botdict"]["tempvals"]['all_current_users']:
            targets.append(target)
    else:
        for target in botcom.triggerargsarray:
            if target in bot.memory["botdict"]["tempvals"]['all_current_users']:
                targets.append(target)

    for target in targets:
        if target in botcom.triggerargsarray:
            botcom.triggerargsarray.remove(target)

    botmessage = spicemanip(bot, botcom.triggerargsarray, 0)
    if not botmessage:
        osd(bot, botcom.instigator, 'notice', "You must specify a message.")
        return

    osd(bot, targets, 'notice', botmessage)


"""
Channel
"""


def bot_command_function_channel(bot, botcom):

    # SubCommand used
    valid_subcommands = ['list', 'op', 'hop', 'voice', 'users']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1) or 'list'
    if subcommand in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(subcommand)

    # list channels
    if subcommand == 'list':
        chanlist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'].keys(), 'andlist')
        osd(bot, botcom.channel_current, 'say', "You can find me in " + chanlist)
        return

    # Channel
    targetchannels = []
    if botcom.triggerargsarray == []:
        if botcom.channel_current.startswith('#'):
            targetchannels.append(botcom.channel_current)
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    elif 'all' in botcom.triggerargsarray:
        for targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
            targetchannels.append(targetchan)
    else:
        for targetchan in botcom.triggerargsarray:
            if targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
                targetchannels.append(targetchan)

    dispmsg = []

    # OP list
    if subcommand.lower() == 'op':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanops'] == []:
                dispmsg.append("There are no Channel Operators for " + str(channeltarget))
            else:
                oplist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanops'], 'andlist')
                dispmsg.append("Channel Operators for " + str(channeltarget) + "  are: " + oplist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # HOP list
    if subcommand.lower() == 'hop':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanhalfops'] == []:
                dispmsg.append("There are no Channel Half Operators for " + str(channeltarget))
            else:
                hoplist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanhalfops'], 'andlist')
                dispmsg.append("Channel Half Operators for " + str(channeltarget) + "  are: " + hoplist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # Voice List
    if subcommand.lower() == 'voice':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanvoices'] == []:
                dispmsg.append("There are no Channel VOICE for " + str(channeltarget))
            else:
                voicelist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanvoices'], 'andlist')
                dispmsg.append("Channel VOICE for " + str(channeltarget) + " are: " + voicelist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # Users List
    if subcommand.lower() == 'users':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['current_users'] == []:
                dispmsg.append("There are no Channel users for " + str(channeltarget))
            else:
                userslist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['current_users'], 'andlist')
                dispmsg.append("Channel users for " + str(channeltarget) + " are: " + userslist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return


"""
Admins
"""


def bot_command_function_admins(bot, botcom):

    targetbots = []
    if botcom.triggerargsarray == []:
        targetbots.append(str(bot.nick))
    elif 'all' in botcom.triggerargsarray:
        for targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            targetbots.append(targetbot)
    else:
        for targetbot in botcom.triggerargsarray:
            if targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                targetbots.append(targetbot)

    dispmsg = []
    for targetbot in targetbots:
        currentbotsadmins = bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['configuration']['core']['admins']
        dispmsg.append(targetbot + " is administered by " + currentbotsadmins)
    osd(bot, botcom.channel_current, 'say', spicemanip(bot, dispmsg, 'andlist'))


"""
Owner
"""


def bot_command_function_owner(bot, botcom):

    targetbots = []
    if botcom.triggerargsarray == []:
        targetbots.append(str(bot.nick))
    elif 'all' in botcom.triggerargsarray:
        for targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            targetbots.append(targetbot)
    else:
        for targetbot in botcom.triggerargsarray:
            if targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                targetbots.append(targetbot)

    dispmsg = []
    for targetbot in targetbots:
        currentbotsowner = bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['configuration']['core']['owner']
        dispmsg.append(targetbot + " is owned by " + currentbotsowner)
    osd(bot, botcom.channel_current, 'say', spicemanip(bot, dispmsg, 'andlist'))


"""
Uptime
"""


def bot_command_function_uptime(bot, botcom):
    delta = datetime.timedelta(seconds=round((datetime.datetime.utcnow() - bot.memory["botdict"]["tempvals"]["uptime"]).total_seconds()))
    osd(bot, botcom.channel_current, 'say', "I've been sitting here for {} and I keep going!".format(delta))


"""
Gender
"""


def bot_command_function_gender(bot, botcom):
    osd(bot, botcom.channel_current, 'say', "My gender is Female")


"""
Can You see me
"""


def bot_command_function_canyouseeme(bot, botcom):
    osd(bot, botcom.channel_current, 'say', botcom.instigator + ", I can see you.")


"""
Testing
"""


def bot_command_function_dict(bot, botcom):
    osd(bot, botcom.channel_current, 'say', str(bot.memory["botdict"]["users"]))
