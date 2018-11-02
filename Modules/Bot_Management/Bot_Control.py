#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example, OP, ADMIN, VOICE, event, rule
import sopel
from sopel import module, tools
import re
import datetime
import git
import ConfigParser
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

GITWIKIURL = "https://github.com/SpiceBot/SpiceBot/wiki"

# TODO add a notification of traceback errors
# TODO add warn functionality
# TODO channel and user commands

"""
# bot.nick do this
"""


@nickname_commands('modules', 'block', 'github', 'on', 'off', 'devmode', 'permfix', 'pip', 'help', 'docs', 'cd', 'dir', 'gitpull')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):
    triggerargsarray = spicemanip(bot, trigger.group(0), 'create')
    triggerargsarray = spicemanip(bot, triggerargsarray, '2+')
    triggerargsarray = spicemanip(bot, triggerargsarray, 'create')
    bot_command_process(bot, trigger, triggerargsarray)


def bot_command_process(bot, trigger, triggerargsarray):

    # Dyno Classes
    botcom = class_create('bot')
    instigator = class_create('instigator')
    botcom.instigator = trigger.nick

    # time
    botcom.now = time.time()

    # User
    botcom = bot_command_users(bot, botcom)

    # Channels
    botcom = bot_command_channels(bot, botcom, trigger)

    # Command Used
    botcom.command_main = spicemanip(bot, triggerargsarray, 1)
    if botcom.command_main in triggerargsarray:
        triggerargsarray.remove(botcom.command_main)
    if botcom.command_main == 'help':
        botcom.command_main = 'docs'
    botcom.triggerargsarray = triggerargsarray
    bot_command_function_run = str('bot_command_function_' + botcom.command_main.lower() + '(bot,trigger,botcom,instigator)')
    eval(bot_command_function_run)


"""
Commands
"""


def bot_command_function_gitpull(bot, trigger, botcom, instigator):

    botcom.directory = get_database_value(bot, bot.nick, 'current_admin_dir') or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    osd(bot, botcom.channel_current, 'say', "attempting to git pull " + botcom.directory)
    g = git.cmd.Git(botcom.directory)
    g.pull()


def bot_command_function_dir(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    botcom.directory = get_database_value(bot, bot.nick, 'current_admin_dir') or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    botcom = bot_list_directory(bot, botcom)
    if botcom.directory == []:
        osd(bot, botcom.channel_current, 'say', "It appears this directory is empty.")
        return
    displaymsgarray = []
    displaymsgarray.append("Current files located in " + str(botcom.directory) + " :")
    for filename, filefoldertype in zip(botcom.directory_listing, botcom.filefoldertype):
        displaymsgarray.append(str("["+filefoldertype.title()+"] ")+str(filename))
    osd(bot, botcom.channel_current, 'say', displaymsgarray)


def bot_command_function_cd(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    validfolderoptions = ['..', 'reset']
    botcom.directory = get_database_value(bot, bot.nick, 'current_admin_dir') or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    botcom = bot_list_directory(bot, botcom)

    for filename, filefoldertype in zip(botcom.directory_listing, botcom.filefoldertype):
        if filefoldertype == 'folder':
            validfolderoptions.append(filename)

    movepath = spicemanip(bot, botcom.triggerargsarray, 0)
    if movepath not in validfolderoptions:
        if movepath in botcom.directory_listing and movepath not in validfolderoptions:
            osd(bot, botcom.channel_current, 'say', "You can't Change Directory into a File!")
        else:
            osd(bot, botcom.channel_current, 'say', "Invalid Folder Path")
        return

    if movepath == "..":
        movepath = os.path.dirname(botcom.directory)
    elif movepath == 'reset':
        movepath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    else:
        movepath = os.path.join(botcom.directory, str(movepath+"/"))

    set_database_value(bot, bot.nick, 'current_admin_dir', str(movepath))

    osd(bot, botcom.channel_current, 'say', "Directory Changed to : " + str(movepath))


def bot_command_function_docs(bot, trigger, botcom, instigator):
    osd(bot, botcom.channel_current, 'say', "Online Docs: " + GITWIKIURL)


def bot_command_function_on(bot, trigger, botcom, instigator):

    target = spicemanip(bot, [x for x in botcom.triggerargsarray if x in botcom.users_all], 1) or botcom.instigator
    if target != botcom.instigator and botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function on other users.")
        return
    bot_opted_users = get_database_value(bot, bot.nick, 'users_opted') or []
    if target in bot_opted_users:
        if target == botcom.instigator:
            osd(bot, botcom.instigator, 'notice', "It looks like you already have " + bot.nick + " " + botcom.command_main+".")
        else:
            osd(bot, botcom.instigator, 'notice', "It looks like " + target + " already has " + bot.nick + " " + botcom.command_main+".")
        return
    if target == botcom.instigator:
        osd(bot, botcom.instigator, 'notice', "It looks like you now have " + bot.nick + " " + botcom.command_main+".")
    else:
        osd(bot, botcom.instigator, 'notice', "It looks like " + target + " now has " + bot.nick + " " + botcom.command_main+".")
    adjust_database_array(bot, bot.nick, target, 'users_opted', 'add')


def bot_command_function_off(bot, trigger, botcom, instigator):
    target = spicemanip(bot, [x for x in botcom.triggerargsarray if x in botcom.users_all], 1) or botcom.instigator
    if target != botcom.instigator and botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function on other users.")
        return
    bot_opted_users = get_database_value(bot, bot.nick, 'users_opted') or []
    if target not in bot_opted_users:
        if target == botcom.instigator:
            osd(bot, botcom.instigator, 'notice', "It looks like you already have " + bot.nick + " " + botcom.command_main+".")
        else:
            osd(bot, botcom.instigator, 'notice', "It looks like " + target + " already has " + bot.nick + " " + botcom.command_main+".")
        return
    if target == botcom.instigator:
        osd(bot, botcom.instigator, 'notice', "It looks like you now have " + bot.nick + " " + botcom.command_main+".")
    else:
        osd(bot, botcom.instigator, 'notice', "It looks like " + target + " now has " + bot.nick + " " + botcom.command_main+".")
    adjust_database_array(bot, bot.nick, target, 'users_opted', 'del')


def bot_command_function_modules(bot, trigger, botcom, instigator):

    # Channel
    channeltarget = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return

    # SubCommand used
    valid_subcommands = ['enable', 'disable', 'list', 'count']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1) or 'list'

    bot_visible_coms = []
    for cmds in bot.command_groups.items():
        for cmd in cmds:
            if str(cmd).endswith("]"):
                for x in cmd:
                    bot_visible_coms.append(x)

    bot_enabled_coms = get_database_value(bot, channeltarget, 'modules_enabled') or []

    if subcommand == 'count':
        osd(bot, botcom.channel_current, 'say', 'There are currently ' + str(len(bot_visible_coms)) + ' custom modules installed.')
        return

    if subcommand == 'list':
        botmessagearray = []
        botmessagearray.append("This is a listing of modules that I can see (E=Enabled, A=Available):")
        for command in bot_visible_coms:
            if command in bot_enabled_coms:
                botmessagearray.append(command+"[E]")
            else:
                botmessagearray.append(command+"[A]")
        osd(bot, botcom.instigator, 'notice', botmessagearray)

    # Enable/Disable
    if subcommand == 'enable' or subcommand == 'disable':

        if botcom.instigator not in botcom.opadmin:
            osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
            return

        module_adjust = spicemanip(bot, [x for x in botcom.triggerargsarray if x in bot_visible_coms or x == 'all'], 1) or 'no_module'
        if module_adjust == 'no_module':
            osd(bot, botcom.instigator, 'notice', "What module do you want to "+str(subcommand)+" for " + channeltarget + "?")
            return

        if module_adjust in bot_enabled_coms and subcommand == 'enable' and module_adjust != 'all':
            osd(bot, botcom.instigator, 'notice', "It looks like "+str(module_adjust)+" is already "+subcommand.lower()+"d for " + channeltarget + "?")
            return

        if module_adjust not in bot_enabled_coms and subcommand == 'disable' and module_adjust != 'all':
            osd(bot, botcom.instigator, 'notice', "It looks like "+str(module_adjust)+" is already "+subcommand.lower()+"d for " + channeltarget + "?")
            return

        if module_adjust == 'all':
            modulesadjustarray = bot_visible_coms
        else:
            modulesadjustarray = [module_adjust]

        if subcommand == 'enable':
            adjust_database_array(bot, channeltarget, modulesadjustarray, 'modules_enabled', 'add')
        else:
            adjust_database_array(bot, channeltarget, modulesadjustarray, 'modules_enabled', 'del')
        osd(bot, botcom.channel_current, 'say', module_adjust + " command(s) should now be "+str(subcommand)+"d for " + channeltarget + ".")


def bot_command_function_block(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    # Channel
    channeltarget = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    if channeltarget in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(channeltarget)

    # SubCommand used
    valid_subcommands = ['current', 'add', 'del']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1) or 'current'

    bot_blocked_users = get_database_value(bot, channeltarget, 'users_blocked') or []

    if subcommand == 'current':
        botmessage = []
        if bot_blocked_users != []:
            botmessage.append("The following users are currently blocked:")
            current_block_list = spicemanip(bot, bot_blocked_users, 'list')
            botmessage.append(str(current_block_list))
        else:
            botmessage.append("No users are currently blocked")
        osd(bot, botcom.channel_current, 'say', botmessage)
        return

    if subcommand == 'add' or subcommand == 'del':
        blocknewlist = []
        if 'all' in botcom.triggerargsarray:
            for user in botcom.users_all:
                if subcommand == 'add' and user not in bot_blocked_users:
                    blocknewlist.append(user)
                if subcommand == 'del' and user in bot_blocked_users:
                    blocknewlist.append(user)
        else:
            for word in botcom.triggerargsarray:
                if word in botcom.users_all and word not in blocknewlist:
                    if subcommand == 'add' and word not in bot_blocked_users:
                        blocknewlist.append(word)
                    if subcommand == 'del' and word in bot_blocked_users:
                        blocknewlist.append(word)

        if blocknewlist == []:
            osd(bot, botcom.instigator, 'notice', "No Valid Users found to block.")
            return

        blocknewlisttext = spicemanip(bot, blocknewlist, 'list')

        if subcommand == 'add':
            adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked', 'add')
            adddelword = "added to"
            osd(bot, botcom.channel_current, 'say', "The following users have been " + adddelword + " the " + channeltarget + " block list: " + blocknewlisttext)
        else:
            adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked', 'del')
            adddelword = "removed from"
            osd(bot, botcom.channel_current, 'say', "The following users have been " + adddelword + " the " + channeltarget + " block list: " + blocknewlisttext)


def bot_command_function_github(bot, trigger, botcom, instigator):

    # main subcom
    valid_main_subcom = ['show', 'block']
    main_subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_main_subcom], 1) or 'show'

    if main_subcommand == 'show':
        osd(bot, botcom.channel_current, 'say', 'Spiceworks IRC Modules     https://github.com/SpiceBot/SpiceBot')
        return

    if main_subcommand == 'block':

        if botcom.instigator not in botcom.opadmin:
            osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
            return

        # Channel
        channeltarget = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith('#')], 1)
        if not channeltarget:
            if botcom.channel_current.startswith('#'):
                channeltarget = botcom.channel_current
            else:
                osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
                return
        if channeltarget in botcom.triggerargsarray:
            botcom.triggerargsarray.remove(channeltarget)

        # SubCommand used
        valid_subcommands = ['current', 'add', 'del']
        subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1) or 'current'

        bot_blocked_users_github = get_database_value(bot, channeltarget, 'users_blocked_github') or []

        if subcommand == 'current':
            botmessage = []
            if bot_blocked_users_github != []:
                botmessage.append("The following users are currently blocked:")
                current_block_list = spicemanip(bot, bot_blocked_users_github, 'list')
                botmessage.append(str(current_block_list))
            else:
                botmessage.append("No users are currently blocked from github.")
            osd(bot, botcom.channel_current, 'say', botmessage)
            return

        if subcommand == 'add' or subcommand == 'del':
            blocknewlist = []
            if 'all' in botcom.triggerargsarray:
                for user in botcom.users_all:
                    if subcommand == 'add' and user not in bot_blocked_users_github:
                        blocknewlist.append(user)
                    if subcommand == 'del' and user in bot_blocked_users_github:
                        blocknewlist.append(user)
            else:
                for word in botcom.triggerargsarray:
                    if word in botcom.users_all and word not in blocknewlist:
                        if subcommand == 'add' and word not in bot_blocked_users_github:
                            blocknewlist.append(word)
                        if subcommand == 'del' and word in bot_blocked_users_github:
                            blocknewlist.append(word)

            if blocknewlist == []:
                osd(bot, botcom.instigator, 'notice', "No Valid Users found to block from github.")
                return

            blocknewlisttext = spicemanip(bot, blocknewlist, 'list')

            if subcommand == 'add':
                adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked_github', 'add')
                adddelword = "added to"
            else:
                adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked_github', 'del')
                adddelword = "removed from"
            osd(bot, botcom.channel_current, 'say', "The following users have been " + adddelword + " the " + channeltarget + " github block list: " + blocknewlisttext)
        return


def bot_command_function_devmode(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.botadmins:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    # Channel
    channeltarget = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    if channeltarget in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(channeltarget)

    # SubCommand used
    valid_subcommands = ['on', 'off']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1)
    if not subcommand:
        osd(bot, botcom.instigator, 'notice', "Do you want devmode on or off in " + channeltarget + "?")
        return

    if subcommand == 'on':
        adjust_database_array(bot, bot.nick, [channeltarget], 'channels_dev', 'add')
    else:
        adjust_database_array(bot, bot.nick, [channeltarget], 'channels_dev', 'del')
    osd(bot, botcom.channel_current, 'say', "devmode should now be " + subcommand + " for " + channeltarget + ".")


def bot_command_function_permfix(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.botadmins:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    os.system("sudo chown -R spicebot:sudo /home/spicebot/.sopel/")
    osd(bot, botcom.channel_current, 'say', "Permissions should now be fixed")


def bot_command_function_pip(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.botadmins:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    pipcoms = ['install', 'remove']
    subcom = spicemanip(bot, [x for x in botcom.triggerargsarray if x in pipcoms], 1) or None
    if not subcom:
        return osd(bot, trigger.sender, 'say', "pip requires a subcommand. Valid options: " + spicemanip(bot, pipcoms, 'andlist'))

    if subcom in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(subcom)

    pippackage = spicemanip(bot, botcom.triggerargsarray, 0)
    if not pippackage:
        return osd(bot, botcom.channel_current, 'say', "You must specify a pip package.")

    installines = []
    previouslysatisfied = []
    for line in os.popen("sudo pip " + str(subcom) + " " + str(pippackage)).read().split('\n'):
        if "Requirement already satisfied:" in str(line):
            packagegood = str(line).split("Requirement already satisfied:", 1)[1]
            packagegood = str(packagegood).split("in", 1)[0]
            previouslysatisfied.append(packagegood)
        else:
            installines.append(str(line))

    if previouslysatisfied != []:
        previouslysatisfiedall = spicemanip(bot, previouslysatisfied, 'andlist')
        installines.insert(0, "The following required packages have already been satisfied: " + previouslysatisfiedall)

    if installines == []:
        return osd(bot, botcom.channel_current, 'action', "has no install log for some reason.")

    for line in installines:
        osd(bot, trigger.sender, 'say', line)
    osd(bot, botcom.channel_current, 'say', "Possibly done.")


"""
dir listing
"""


def bot_list_directory(bot, botcom):
    botcom.directory_listing = []
    botcom.filefoldertype = []
    for filename in os.listdir(botcom.directory):
        botcom.directory_listing.append(filename)
        joindpath = os.path.join(botcom.directory, filename)
        if os.path.isfile(joindpath):
            botcom.filefoldertype.append("file")
        else:
            botcom.filefoldertype.append("folder")
    return botcom


def bot_config_directory(bot, botcom):
    botcom.config_listing = []
    networkname = str(bot.config.core.user.split("/", 1)[1] + "/")
    validconfigsdir = str("/home/spicebot/.sopel/" + bot.nick + "/System-Files/Configs/" + networkname)
    for filename in os.listdir(validconfigsdir):
        filenameminuscfg = str(filename).replace(".cfg", "")
        botcom.config_listing.append(filenameminuscfg)
    return botcom


def bot_target_admins(bot, targetbot):
    targetbotadmins = []
    checkdirectory = os.path.join("/home/spicebot/.sopel/", targetbot)
    if os.path.isdir(checkdirectory):
        networkname = str(bot.config.core.user.split("/", 1)[1] + "/")
        configfile = str("/home/spicebot/.sopel/" + targetbot + "/System-Files/Configs/" + networkname + targetbot + ".cfg")
        config = ConfigParser.ConfigParser()
        config.read(configfile)
        owner = config.get("core", "owner")
        targetbotadmins.append(owner)
        admins = config.get("core", "admins")
        admins = admins.split(",")
        for admin in admins:
            if admin not in targetbotadmins:
                targetbotadmins.append(admin)
    return targetbotadmins
