import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example, OP, HALFOP, ADMIN, VOICE, event, rule
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

import pandas as pd
import json

# author deathbybandaid

valid_command_prefix = ['.', '!', ',']
valid_com_types = ['simple', 'target', 'fillintheblank']

quick_coms_dir = "Quicks/"
quick_coms_path = os.path.join(moduledir, quick_coms_dir)

botcom_dict = {
                # Some values don't get saved to the database, but stay in memory
                "tempvals": {

                            # Indicate if we need to pull the dict from the database
                            "coms_loaded": False,

                            # Loaded configs
                            "commands_loaded": [],

                            # Commands list
                            "commands": {},

                            # Alternate Commands, duplicate of above
                            "alt_commands": {},

                            # list of channels the bot is in
                            "channels_list": [],

                            # Other bots
                            "bots_list": [],

                            # current users
                            "current_users": [],

                            # offline users
                            "offline_users": [],

                            # bot owner users
                            "bot_owner": [],

                            # bot admin users
                            "bot_admins": [],

                            # chan OP
                            "chanops": [],

                            # chan HALFOP
                            "chanhalfops": [],

                            # chan VOICE
                            "chanvoices": [],

                            # players that can't play
                            "cantplayarray": [],

                            # End of Temp Vals
                            },

                # Static content
                "static": {},

                # Users lists
                "users": {
                            "users_all": [],
                            },

                # channels list
                "channels": {
                                "game_enabled": [],
                                "devmode_enabled": []

                                },
                }


@rule('(.*)')
@sopel.module.thread(True)
def watcher(bot, trigger):
    if not str(trigger).startswith(tuple(valid_command_prefix)):
        return

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # Load global dict
    open_botcomdict(bot, botcom)

    # Fetch commands listing
    command_configs(bot, botcom)

    # Channel Listing
    botcom = botcom_command_channels(bot, botcom, trigger)

    # Basic User List
    botcom = botcom_command_users(bot, botcom)

    # Bots can't run commands
    if trigger.nick.lower() in botcom.botcomdict['tempvals']['bots_list']:
        return

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, 'create')

    # command issued, check if valid
    botcom.dotcommand = spicemanip(bot, botcom.triggerargsarray, 1).lower()[1:]
    if botcom.dotcommand not in botcom.botcomdict['tempvals']['commands'].keys():
        return

    # remainder, if any is the new arg list
    botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+')

    # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
    if not botcom.dotcommand:
        return

    # execute function based on command type
    botcom.commandtype = botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["type"].lower()

    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    for command_split_partial in commands_array:
        botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')

        command_function_run = str('botfunction_' + botcom.commandtype + '(bot, trigger, botcom)')
        eval(command_function_run)

    # Save open global dictionary at the end of each usage
    save_botcomdict(bot, botcom)


# Simple quick replies
def botfunction_simple(bot, trigger, botcom):

    specified = None
    if str(spicemanip(bot, botcom.triggerargsarray, 1)).isdigit():
        specified = spicemanip(bot, botcom.triggerargsarray, 1)
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    if not isinstance(botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"], list):
        reply = botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"]
    elif specified:
        if int(specified) > len(botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"]):
            specified = len(botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"])
        reply = spicemanip(bot, botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"], specified)
    else:
        reply = spicemanip(bot, botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"], 'random')
    osd(bot, trigger.sender, 'say', reply)


# Quick replies with a target person TODO use the targetfinder logic
def botfunction_target(bot, trigger, botcom):

    # target is the first arg given
    target = spicemanip(bot, botcom.triggerargsarray, 1)

    # handling for no target
    if not target:

        specified = None
        if str(spicemanip(bot, botcom.triggerargsarray, 1)).isdigit():
            specified = spicemanip(bot, botcom.triggerargsarray, 1)
            botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

        # Seperate reply for no input
        if "noinputreply" in botcom.botcomdict['tempvals']['commands'][botcom.dotcommand].keys():
            if not isinstance(botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["noinputreply"], list):
                reply = botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["noinputreply"]
            elif specified:
                if int(specified) > len(botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["noinputreply"]):
                    specified = len(botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["noinputreply"])
                reply = spicemanip(bot, botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["noinputreply"], specified)
            else:
                reply = spicemanip(bot, botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["noinputreply"], 'random')
            return osd(bot, trigger.sender, 'say', reply)

        # backup target, usually trigger.nick
        if "backuptarget" in botcom.botcomdict['tempvals']['commands'][botcom.dotcommand].keys():
            target = botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["backuptarget"]
            if target == 'instigator':
                target = botcom.instigator

        # still no target
        if not target and "backuptarget" not in botcom.botcomdict['tempvals']['commands'][botcom.dotcommand].keys():
            reply = "This command requires a target"
            return osd(bot, trigger.nick, 'notice', reply)

    # remove target
    if target in botcom.triggerargsarray:
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    specified = None
    if str(spicemanip(bot, botcom.triggerargsarray, 1)).isdigit():
        specified = spicemanip(bot, botcom.triggerargsarray, 1)
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    # cannot target bots
    if target in botcom.botcomdict["tempvals"]['bots_list']:
        reply = nick_actual(bot, target) + " is a bot and cannot be targeted."
        return osd(bot, trigger.nick, 'notice', reply)

    # Not a valid user
    if target not in botcom.botcomdict["users"]['users_all']:
        reply = "I don't know who that is."
        return osd(bot, trigger.nick, 'notice', reply)

    # User offline
    if target in botcom.botcomdict["users"]['users_all'] and target not in botcom.botcomdict["tempvals"]['current_users']:
        reply = "It looks like " + nick_actual(bot, target) + " is offline right now!"
        return osd(bot, trigger.nick, 'notice', reply)

    if botcom.channel_priv and target != trigger.nick:
        reply = "Leave " + nick_actual(bot, target) + " out of this private conversation!"
        return osd(bot, trigger.nick, 'notice', reply)

    if target in botcom.botcomdict["tempvals"]['current_users'] and target not in bot.privileges[trigger.sender].keys():
        reply = "It looks like " + nick_actual(bot, target) + " is online right now, but in a different channel."
        return osd(bot, trigger.nick, 'notice', reply)

    if not isinstance(botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"], list):
        reply = botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"]
    elif specified:
        if int(specified) > len(botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"]):
            specified = len(botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"])
        reply = spicemanip(bot, botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"], specified)
    else:
        reply = spicemanip(bot, botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"], 'random')
    reply = reply.replace("$target", target)
    osd(bot, trigger.sender, 'say', reply)


# Quick replies with a fillblank person TODO use the targetfinder logic
def botfunction_fillintheblank(bot, trigger, botcom):

    specified = None
    if str(spicemanip(bot, botcom.triggerargsarray, 1)).isdigit():
        specified = spicemanip(bot, botcom.triggerargsarray, 1)
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    fillblank = spicemanip(bot, botcom.triggerargsarray, 0)
    if not fillblank:
        if "noinputreply" in botcom.botcomdict['tempvals']['commands'][botcom.dotcommand].keys():
            reply = botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["noinputreply"]
        elif specified:
            if int(specified) > len(botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"]):
                specified = len(botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"])
            reply = spicemanip(bot, botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"], specified)
        else:
            reply = "No input provided"
    else:
        reply = botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"].replace("$fillblank", target)

    reply = botcom.botcomdict['tempvals']['commands'][botcom.dotcommand]["reply"].replace("$fillblank", fillblank)
    osd(bot, trigger.sender, 'say', reply)


"""
Command Config Files
"""


# Command configs
def command_configs(bot, botcom):

    # Don't load commands if already loaded
    if botcom.botcomdict['tempvals']['commands_loaded'] != []:
        return

    # iterate over organizational folders
    for quick_coms_type in os.listdir(quick_coms_path):

        # iterate over files within
        coms_type_file_path = os.path.join(quick_coms_path, quick_coms_type)
        for comconf in os.listdir(coms_type_file_path):

            # check if command file is already in the list
            if comconf not in botcom.botcomdict['tempvals']['commands_loaded']:

                # add file to already processed
                botcom.botcomdict['tempvals']['commands_loaded'].append(comconf)

                # Read dictionary from file, if not, enable an empty dict
                inf = open(os.path.join(coms_type_file_path, comconf), 'r')
                try:
                    dict_from_file = eval(inf.read())
                except SyntaxError:
                    dict_from_file = dict()

                # Close File
                inf.close()

                # default command to filename
                if "validcoms" not in dict_from_file.keys():
                    dict_from_file["validcoms"] = [comconf]
                elif dict_from_file["validcoms"] == []:
                    dict_from_file["validcoms"] = [comconf]
                elif not isinstance(dict_from_file['validcoms'], list):
                    dict_from_file["validcoms"] = [dict_from_file["validcoms"]]

                # check that type is set
                if "type" not in dict_from_file.keys():
                    dict_from_file["type"] = quick_coms_type.lower()
                if dict_from_file["type"] not in valid_com_types:
                    dict_from_file["type"] = 'simple'
                    dict_from_file["reply"] = "This command is not setup with a proper 'type'."

                # check that reply is set
                if "reply" not in dict_from_file.keys():
                    dict_from_file["reply"] = "Reply missing"

                # iterate over all valid commands
                for vcom in dict_from_file["validcoms"]:
                    if vcom not in botcom.botcomdict['tempvals']['commands'].keys():
                        botcom.botcomdict['tempvals']['commands'][vcom] = dict_from_file


"""
Botcomdict
"""


def open_botcomdict(bot, botcom):

    # open global dict as part of botcom class
    global botcom_dict
    botcom.botcomdict = botcom_dict

    # don't pull from database if already open
    if not botcom.botcomdict["tempvals"]["coms_loaded"]:
        opendict = botcom_dict.copy()
        dbbotcomdict = get_database_value(bot, 'botcom_records', 'botcom_dict') or dict()
        opendict = merge_botcomdict(opendict, dbbotcomdict)
        botcom.botcomdict.update(opendict)
        botcom.botcomdict["tempvals"]['coms_loaded'] = True


def save_botcomdict(bot, botcom):

    # copy dict to not overwrite
    savedict = botcom.botcomdict.copy()

    # Values to not save to database
    savedict_del = ['tempvals', 'static']
    for dontsave in savedict_del:
        if dontsave in savedict.keys():
            del savedict[dontsave]

    # save to database
    set_database_value(bot, 'botcom_records', 'botcom_dict', savedict)


def merge_botcomdict(a, b, path=None):
    "merges b into a"
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_botcomdict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


"""
Channels
"""


def botcom_command_channels(bot, botcom, trigger):

    # current Channels
    botcom.channel_current = trigger.sender

    # determine the type of channel
    if not botcom.channel_current.startswith("#"):
        botcom.channel_priv = 1
        botcom.channel_real = 0
    else:
        botcom.channel_priv = 0
        botcom.channel_real = 1

    # All channels the bot is in
    if botcom.botcomdict["tempvals"]['channels_list'] == []:
        for channel in bot.channels:
            botcom.botcomdict["tempvals"]['channels_list'].append(channel)

    # Development mode
    botcom.dev_bypass = 0  # TODO not needed
    if botcom.channel_current.lower() in [x.lower() for x in botcom.botcomdict['channels']['devmode_enabled']]:
        botcom.dev_bypass = 1
    return botcom


"""
Users
"""


@event('JOIN')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_return(bot, trigger):

    instigator = trigger.nick

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # Load Game Players and map
    open_botcomdict(bot, botcom)

    # Channel Listing
    botcom = botcom_command_channels(bot, botcom, trigger)

    # Bacic User List
    botcom = botcom_command_users(bot, botcom)

    if instigator not in botcom.botcomdict["tempvals"]['current_users']:
        if instigator not in botcom.botcomdict['tempvals']['commands'].keys() and instigator not in botcom.botcomdict['tempvals']['alt_commands'].keys() and instigator not in botcom.botcomdict['tempvals']['bots_list']:
            botcom.botcomdict["tempvals"]['current_users'].append(instigator)

    if instigator not in botcom.botcomdict["users"]['users_all']:
        botcom.botcomdict["users"]['users_all'].append(instigator)

    if instigator in botcom.botcomdict["tempvals"]['offline_users']:
        botcom.botcomdict["tempvals"]['offline_users'].remove(instigator)


@event('QUIT', 'PART')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_leave(bot, trigger):

    instigator = trigger.nick

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # Load Game Players and map
    open_botcomdict(bot, botcom)

    # Channel Listing
    botcom = botcom_command_channels(bot, botcom, trigger)

    # Bacic User List
    botcom = botcom_command_users(bot, botcom)

    if instigator in botcom.botcomdict["tempvals"]['current_users']:
        botcom.botcomdict["tempvals"]['current_users'].remove(instigator)

    if instigator not in botcom.botcomdict["tempvals"]['offline_users']:
        botcom.botcomdict["tempvals"]['offline_users'].append(instigator)


def botcom_command_users(bot, botcom):

    # Userlists that typically don't change when bot is running
    if botcom.botcomdict["tempvals"]['bots_list'] == []:
        botcom.botcomdict["tempvals"]['bots_list'] = bot_config_names(bot)

    if botcom.botcomdict["tempvals"]['bot_owner'] == []:
        for user in bot.config.core.owner:
            if user not in botcom.botcomdict["tempvals"]['bot_owner']:
                botcom.botcomdict["tempvals"]['bot_owner'].append(user)

    if botcom.botcomdict["tempvals"]['bot_admins'] == []:
        for user in bot.config.core.admins:
            if user not in botcom.botcomdict["tempvals"]['bot_admins']:
                botcom.botcomdict["tempvals"]['bot_admins'].append(user)

    # users that cannot be part of the game
    if botcom.botcomdict["tempvals"]['cantplayarray'] == []:
        cantplayarrays = ["botcom.botcomdict['tempvals']['commands'].keys()", "botcom.botcomdict['tempvals']['alt_commands'].keys()", "botcom.botcomdict['tempvals']['bots_list']"]
        for nicklist in cantplayarrays:
            currentnicklist = eval(nicklist)
            for x in currentnicklist:
                if x not in botcom.botcomdict["tempvals"]['cantplayarray']:
                    botcom.botcomdict["tempvals"]['cantplayarray'].append(x)

    for channelcheck in botcom.botcomdict["tempvals"]['channels_list']:
        for user in bot.privileges[channelcheck].keys():
            if user not in botcom.botcomdict["tempvals"]['cantplayarray']:

                # Start with Channel permissions
                if bot.privileges[channelcheck][user] == OP:
                    if user not in botcom.botcomdict["tempvals"]['chanops']:
                        botcom.botcomdict["tempvals"]['chanops'].append(user)

                elif bot.privileges[channelcheck][user] == HALFOP:
                    if user not in botcom.botcomdict["tempvals"]['chanhalfops']:
                        botcom.botcomdict["tempvals"]['chanhalfops'].append(user)

                elif bot.privileges[channelcheck][user] == VOICE:
                    if user not in botcom.botcomdict["tempvals"]['chanvoices']:
                        botcom.botcomdict["tempvals"]['chanvoices'].append(user)

                # user lists
                if user not in botcom.botcomdict["tempvals"]['current_users']:
                    botcom.botcomdict["tempvals"]['current_users'].append(user)

    for user in botcom.botcomdict["tempvals"]['current_users']:
        if user not in botcom.botcomdict["tempvals"]['cantplayarray']:
            if user not in botcom.botcomdict["users"]['users_all']:
                botcom.botcomdict["users"]['users_all'].append(user)

    for user in botcom.botcomdict["users"]['users_all']:
        if user not in botcom.botcomdict["tempvals"]['cantplayarray']:
            if user not in botcom.botcomdict["tempvals"]['current_users']:
                if user not in botcom.botcomdict["tempvals"]['offline_users']:
                    botcom.botcomdict["tempvals"]['offline_users'].append(user)

    return botcom


# Bot Nicks
def bot_config_names(bot):
    config_listing = []
    networkname = str(bot.config.core.user.split("/", 1)[1] + "/")
    validconfigsdir = str("/home/spicebot/.sopel/" + bot.nick + "/System-Files/Configs/" + networkname)
    for filename in os.listdir(validconfigsdir):
        filenameminuscfg = str(filename).replace(".cfg", "")
        config_listing.append(filenameminuscfg)
    return config_listing
