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

quick_coms_dir = "Quicks/"
quick_coms_path = os.path.join(moduledir, quick_coms_dir)


# TODO a way to import stuff like this directly from other files?
# TODO redirect dict, this == that
commandsdict = {
                "testa": {
                            "type": "simple",
                            "reply": "This is a test of a quick reply to a command.",
                            },
                "testb": {
                            "type": "target",
                            "reply": "This is a target test directed at $target.",
                            },
                "testc": {
                            "type": "target",
                            "reply": "This is a target test directed at $target. Hopefully $target enjoys that kid of thing",
                            },
                "testd": {
                            "type": "test",
                            "reply": "grrrr",
                            },
                }

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
    bot.say(str(trigger))

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # Load global dict
    open_botcomdict(bot, botcom)

    # Channel Listing
    botcom = botcom_command_channels(bot, botcom, trigger)

    # Basic User List
    botcom = botcom_command_users(bot, botcom)

    # Bots can't run commands
    if trigger.nick.lower() in botcom.botcomdict['tempvals']['bots_list']:
        return

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, 'create')

    # command issued
    botcom.dotcommand = spicemanip(bot, botcom.triggerargsarray, 1).lower()[1:]

    # Fetch commands listing
    command_configs(bot, botcom)

    # remainder, if any is the new arg list
    botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+')

    # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
    if not botcom.dotcommand:
        return

    # Save open global dictionary at the end of each usage
    save_botcomdict(bot, botcom)


# Command configs
def command_configs(bot, botcom):
    for quick_coms_type in os.listdir(quick_coms_path):

        coms_type_file_path = os.path.join(quick_coms_path, quick_coms_type)
        for comconf in os.listdir(coms_type_file_path):
            if comconf not in botcom.botcomdict['tempvals']['commands_loaded']:
                botcom.botcomdict['tempvals']['commands_loaded'].append(comconf)
                inf = open(os.path.join(coms_type_file_path, comconf), 'r')
                try:
                    dict_from_file = eval(inf.read())
                except SyntaxError:
                    dict_from_file = dict()
                inf.close()
            # botcom.botcomdict['tempvals']['commands'].keys()


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


def watchallthethings(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # open global dict as part of botcom class
    global commandsdict
    botcom.commandsdict = commandsdict

    # does not apply to bots
    if trigger.nick.lower() in bot_config_names(bot):
        return

    # make sure first word starts with "."
    if not str(spicemanip(bot, trigger, 1)).startswith("."):
        return

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, 'create')

    # command issued
    botcom.dotcommand = spicemanip(bot, botcom.triggerargsarray, 1).lower().replace(".", "")

    # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
    if not botcom.dotcommand:
        return

    # remainder, if any is the new arg list
    botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+')

    # if there is nt a nested dictionary for the command requested, then privmsg and exit
    if botcom.dotcommand not in botcom.commandsdict.keys():
        return  # temp TODO
        osd(bot, trigger.sender, 'say', "I don't seem to have a command for " + botcom.dotcommand)
        return

    # execute function based on command type
    botcom.commandtype = botcom.commandsdict[botcom.dotcommand]["type"]
    command_function_run = str('botfunction_' + botcom.commandtype + '(bot, trigger, botcom)')
    try:
        eval(command_function_run)
    except NameError:
        osd(bot, trigger.sender, 'say', "This command is not setup with a proper 'type'.")


# Simple quick replies
def botfunction_simple(bot, trigger, botcom):
    reply = botcom.commandsdict[botcom.dotcommand]["reply"]
    osd(bot, trigger.sender, 'say', reply)


# Quick replies with a target person TODO use the targetfinder logic
def botfunction_target(bot, trigger, botcom):

    target = spicemanip(bot, botcom.triggerargsarray, 1)
    if not target:
        osd(bot, trigger.sender, 'say', "No target provided")
        return

    reply = botcom.commandsdict[botcom.dotcommand]["reply"].replace("$target", target)
    osd(bot, trigger.sender, 'say', reply)


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
