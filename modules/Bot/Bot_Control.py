#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
## sopel imports
import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example, OP, ADMIN, VOICE, event, rule
import sopel
from sopel import module, tools
import re
import git
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *
log_path = "data/templog.txt"
log_file_path = os.path.join(moduledir, log_path)

## TODO add a notification of traceback errors
## TODO add warn functionality
## TODO channel and user commands

"""
## bot.nick do this
"""
@nickname_commands('modules','msg','action','block','gitblock','on','off','devmode','update','restart','permfix','debug','pip','channel')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):
    botcom = botcom_class()
    triggerargsarray = get_trigger_arg(bot, trigger.group(0), 'create')
    triggerargsarray = get_trigger_arg(bot, triggerargsarray, '2+')
    triggerargsarray = get_trigger_arg(bot, triggerargsarray, 'create')
    bot_command_process(bot,trigger,botcom,triggerargsarray)

def bot_command_process(bot,trigger,botcom,triggerargsarray):

    ## Basics
    botcom.instigator = trigger.nick
    botcom.channel_current = trigger.sender
    if not botcom.channel_current.startswith("#"):
        botcom.channel_priv = 1
        botcom.channel_real = 0
    else:
        botcom.channel_priv = 0
        botcom.channel_real = 1
    botcom.service = bot.nick
    ## time
    botcom.now = time.time()
    botcom = bot_command_users(bot,botcom)
    botcom = bot_command_channels(bot,botcom)

    ## Command Used
    botcom.command_main = get_trigger_arg(bot, triggerargsarray, 1)
    if botcom.command_main in triggerargsarray:
        triggerargsarray.remove(botcom.command_main)
    bot_command_function_run = str('bot_command_function_' + botcom.command_main.lower() + '(bot,trigger,botcom,triggerargsarray)')
    eval(bot_command_function_run)

"""
Commands
"""

def bot_command_function_channel(bot,trigger,botcom,triggerargsarray):

    ## SubCommand used
    valid_subcommands = ['list','op','voice']
    subcommand = get_trigger_arg(bot, [x for x in triggerargsarray if x in valid_subcommands], 1) or 'list'

    ## list channels
    if subcommand == 'list':
        channelarray = []
        for c in bot.channels:
            channelarray.append(c)
        chanlist = get_trigger_arg(bot, channelarray, 'list')
        onscreentext(bot, ['say'], "You can find me in " + chanlist)
        return

    ## OP list
    if subcommand.lower() == 'op':
        oplist = get_trigger_arg(bot, botcom.chanops, 'list')
        osd_notice(bot, botcom.instigator, "Channel Operators are: " + oplist)
        return

    ## Voice List
    if subcommand.lower() == 'voice':
        voicelist = get_trigger_arg(bot, botcom.chanvoice, 'list')
        osd_notice(bot, botcom.instigator, "Channel VOICE are: " + voicelist)
        return

def bot_command_function_on(bot,trigger,botcom,triggerargsarray):

    target = get_trigger_arg(bot, [x for x in triggerargsarray if x in botcom.users_all], 1) or botcom.instigator
    if target != botcom.instigator and botcom.instigator not in botcom.opadmin:
        osd_notice(bot, botcom.instigator, "You are unauthorized to use this function on other users.")
        return
    bot_opted_users = get_database_value(bot, bot.nick, 'users_blocked') or []
    if target not in bot_opted_users:
        if target == botcom.instigator:
            osd_notice(bot, botcom.instigator, "It looks like you already have " + bot.nick + " " + botcom.command_main+".")
        else:
            osd_notice(bot, botcom.instigator, "It looks like " + target + " already has " + bot.nick + " " + botcom.command_main+".")
        return
    adjust_database_array(bot, bot.nick, target, 'users_opted', 'add')

def bot_command_function_off(bot,trigger,botcom,triggerargsarray):
    target = get_trigger_arg(bot, [x for x in triggerargsarray if x in botcom.users_all], 1) or botcom.instigator
    if target != botcom.instigator and botcom.instigator not in botcom.opadmin:
        osd_notice(bot, botcom.instigator, "You are unauthorized to use this function on other users.")
        return
    bot_opted_users = get_database_value(bot, channeltarget, 'users_blocked') or []
    if target in bot_blocked_users:
        if target == botcom.instigator:
            osd_notice(bot, botcom.instigator, "It looks like you already have " + bot.nick + " " + botcom.command_main+".")
        else:
            osd_notice(bot, botcom.instigator, "It looks like " + target + " already has " + bot.nick + " " + botcom.command_main+".")
        return
    adjust_database_array(bot, bot.nick, target, 'users_opted', 'del')

def bot_command_function_modules(bot,trigger,botcom,triggerargsarray):

    ## Channel
    channeltarget = get_trigger_arg(bot, [x for x in triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd_notice(bot, botcom.instigator, "You must specify a valid channel.")
            return

    ## SubCommand used
    valid_subcommands = ['enable','disable','list']
    subcommand = get_trigger_arg(bot, [x for x in triggerargsarray if x in valid_subcommands], 1) or 'list'

    bot_visible_coms = []
    for cmds in bot.command_groups.items():
        for cmd in cmds:
            if str(cmd).endswith("]"):
                for x in cmd:
                    bot_visible_coms.append(x)

    bot_enabled_coms = get_database_value(bot, channeltarget, 'modules_enabled') or []

    if subcommand == 'list':
        botmessagearray = []
        botmessagearray.append("This is a listing of modules that I can see (E=Enabled, A=Available):")
        for command in bot_visible_coms:
            if command in bot_enabled_coms:
                botmessagearray.append(command+"[E]")
            else:
                botmessagearray.append(command+"[A]")
        osd_notice(bot, botcom.instigator, botmessagearray)

    ## Enable/Disable
    if subcommand == 'enable' or subcommand == 'disable':
        if botcom.instigator not in botcom.opadmin:
            osd_notice(bot, botcom.instigator, "You are unauthorized to use this function.")
            return

        module_adjust = get_trigger_arg(bot, [x for x in triggerargsarray if x in bot_visible_coms or x == 'all'], 1) or 'no_module'
        if module_adjust == 'no_module':
            osd_notice(bot, botcom.instigator, "What module do you want to "+str(subcommand)+" for " + channeltarget + "?")
            return

        if module_adjust in bot_enabled_coms and subcommand == 'enable' and module_adjust != 'all':
            osd_notice(bot, botcom.instigator, "It looks like "+str(module_adjust)+" is already "+subcommand.lower()+"d for " + channeltarget + "?")
            return

        if module_adjust not in bot_enabled_coms and subcommand == 'disable' and module_adjust != 'all':
            osd_notice(bot, botcom.instigator, "It looks like "+str(module_adjust)+" is already "+subcommand.lower()+"d for " + channeltarget + "?")
            return

        if module_adjust == 'all':
            modulesadjustarray = bot_visible_coms
        else:
            modulesadjustarray = [module_adjust]

        if subcommand == 'enable':
            adjust_database_array(bot, channeltarget, modulesadjustarray, 'modules_enabled', 'add')
        else:
            adjust_database_array(bot, channeltarget, modulesadjustarray, 'modules_enabled', 'del')
        onscreentext(bot, ['say'], module_adjust + " command(s) should now be "+str(subcommand)+"d for " + channeltarget + ".")

def bot_command_function_msg(bot,trigger,botcom,triggerargsarray):

    if botcom.instigator not in botcom.opadmin:
        osd_notice(bot, botcom.instigator, "You are unauthorized to use this function.")
        return

    ## Channel
    channeltarget = get_trigger_arg(bot, [x for x in triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd_notice(bot, botcom.instigator, "You must specify a valid channel.")
            return
    if channeltarget in triggerargsarray:
        triggerargsarray.remove(channeltarget)

    botmessage = get_trigger_arg(bot, triggerargsarray, 0)
    if not botmessage:
        osd_notice(bot, botcom.instigator, "You must specify a message.")
        return
    onscreentext(bot, [channeltarget], botmessage)
#test
def bot_command_function_action(bot,trigger,botcom,triggerargsarray):

    if botcom.instigator not in botcom.opadmin:
        osd_notice(bot, botcom.instigator, "You are unauthorized to use this function.")
        return

    ## Channel
    channeltarget = get_trigger_arg(bot, [x for x in triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd_notice(bot, botcom.instigator, "You must specify a valid channel.")
            return
    if channeltarget in triggerargsarray:
        triggerargsarray.remove(channeltarget)

    botmessage = get_trigger_arg(bot, triggerargsarray, 0)
    if not botmessage:
        osd_notice(bot, botcom.instigator, "You must specify a message.")
        return
    onscreentext_action(bot, [channeltarget], botmessage)

def bot_command_function_block(bot,trigger,botcom,triggerargsarray):

    if botcom.instigator not in botcom.opadmin:
        osd_notice(bot, botcom.instigator, "You are unauthorized to use this function.")
        return

    ## Channel
    channeltarget = get_trigger_arg(bot, [x for x in triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd_notice(bot, botcom.instigator, "You must specify a valid channel.")
            return
    if channeltarget in triggerargsarray:
        triggerargsarray.remove(channeltarget)

    ## SubCommand used
    valid_subcommands = ['current','add','del']
    subcommand = get_trigger_arg(bot, [x for x in triggerargsarray if x in valid_subcommands], 1) or 'current'

    bot_blocked_users = get_database_value(bot, channeltarget, 'users_blocked') or []

    if subcommand == 'current':
        botmessage = []
        if bot_blocked_users != []:
            botmessage.append("The following users are currently blocked:")
            current_block_list = get_trigger_arg(bot, bot_blocked_users, 'list')
            botmessage.append(str(current_block_list))
        else:
            botmessage.append("No users are currently blocked")
        onscreentext(bot, ['say'], botmessage)
        return

    if subcommand == 'add' or subcommand == 'del':
        blocknewlist = []
        if 'all' in triggerargsarray:
            for user in botcom.users_all:
                if subcommand == 'add' and user not in bot_blocked_users:
                    blocknewlist.append(user)
                if subcommand == 'del' and user in bot_blocked_users:
                    blocknewlist.append(user)
        else:
            for word in triggerargsarray:
                if word in botcom.users_all and word not in blocknewlist:
                    if subcommand == 'add' and word not in bot_blocked_users:
                        blocknewlist.append(word)
                    if subcommand == 'del' and word in bot_blocked_users:
                        blocknewlist.append(word)

        if blocknewlist == []:
            osd_notice(bot, botcom.instigator, "No Valid Users found to block.")
            return

        blocknewlisttext = get_trigger_arg(bot, blocknewlist, 'list')

        if subcommand == 'add':
            adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked', 'add')
            adddelword = "added to"
            onscreentext(bot, ['say'], "The following users have been " + adddelword + " the " + channeltarget + " block list: "+ blocknewlisttext)
        else:
            adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked', 'del')
            adddelword = "removed from"
            onscreentext(bot, ['say'], "The following users have been " + adddelword + " the " + channeltarget + " block list: "+ blocknewlisttext)

def bot_command_function_gitblock(bot,trigger,botcom,triggerargsarray):

    if botcom.instigator not in botcom.opadmin:
        osd_notice(bot, botcom.instigator, "You are unauthorized to use this function.")
        return

    ## Channel
    channeltarget = get_trigger_arg(bot, [x for x in triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd_notice(bot, botcom.instigator, "You must specify a valid channel.")
            return
    if channeltarget in triggerargsarray:
        triggerargsarray.remove(channeltarget)

    ## SubCommand used
    valid_subcommands = ['current','add','del']
    subcommand = get_trigger_arg(bot, [x for x in triggerargsarray if x in valid_subcommands], 1) or 'current'

    bot_blocked_users_github = get_database_value(bot, channeltarget, 'users_blocked_github') or []

    if subcommand == 'current':
        botmessage = []
        if bot_blocked_users_github != []:
            botmessage.append("The following users are currently blocked:")
            current_block_list = get_trigger_arg(bot, bot_blocked_users_github, 'list')
            botmessage.append(str(current_block_list))
        else:
            botmessage.append("No users are currently blocked from github.")
        onscreentext(bot, ['say'], botmessage)
        return

    if subcommand == 'add' or subcommand == 'del':
        blocknewlist = []
        if 'all' in triggerargsarray:
            for user in botcom.users_all:
                if subcommand == 'add' and user not in bot_blocked_users_github:
                    blocknewlist.append(user)
                if subcommand == 'del' and user in bot_blocked_users_github:
                    blocknewlist.append(user)
        else:
            for word in triggerargsarray:
                if word in botcom.users_all and word not in blocknewlist:
                    if subcommand == 'add' and word not in bot_blocked_users_github:
                        blocknewlist.append(word)
                    if subcommand == 'del' and word in bot_blocked_users_github:
                        blocknewlist.append(word)

        if blocknewlist == []:
            osd_notice(bot, botcom.instigator, "No Valid Users found to block from github.")
            return

        blocknewlisttext = get_trigger_arg(bot, blocknewlist, 'list')

        if subcommand == 'add':
            adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked_github', 'add')
            adddelword = "added to"
            onscreentext(bot, ['say'], "The following users have been " + adddelword + " the " + channeltarget + " github block list: "+ blocknewlisttext)
        else:
            adjust_database_array(bot, channeltarget, blocknewlist, 'users_blocked_github', 'del')
            adddelword = "removed from"
            onscreentext(bot, ['say'], "The following users have been " + adddelword + " the " + channeltarget + " github block list: "+ blocknewlisttext)

def bot_command_function_devmode(bot,trigger,botcom,triggerargsarray):

    if botcom.instigator not in botcom.botadmins:
        osd_notice(bot, botcom.instigator, "You are unauthorized to use this function.")
        return

    ## Channel
    channeltarget = get_trigger_arg(bot, [x for x in triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd_notice(bot, botcom.instigator, "You must specify a valid channel.")
            return
    if channeltarget in triggerargsarray:
        triggerargsarray.remove(channeltarget)

    ## SubCommand used
    valid_subcommands = ['on','off']
    subcommand = get_trigger_arg(bot, [x for x in triggerargsarray if x in valid_subcommands], 1)
    if not subcommand:
        osd_notice(bot, botcom.instigator, "Do you want devmode on or off in " + channeltarget + "?")
        return

    if subcommand == 'on':
        adjust_database_array(bot, bot.nick, [channeltarget], 'channels_dev', 'add')
    else:
        adjust_database_array(bot, bot.nick, [channeltarget], 'channels_dev', 'del')
    onscreentext(bot, ['say'], "devmode should now be " + subcommand + " for " + channeltarget + ".")

def bot_command_function_update(bot,trigger,botcom,triggerargsarray):
    for channel in bot.channels:
        onscreentext(bot, [channel], trigger.nick + " commanded me to update from Github and restart. Be Back Soon!")
    update(bot, trigger)
    restart(bot, trigger, botcom.service)

def bot_command_function_restart(bot,trigger,botcom,triggerargsarray):
    for channel in bot.channels:
        onscreentext(bot, [channel], trigger.nick + " commanded me to restart. Be Back Soon!")
    restart(bot, trigger, service)

def bot_command_function_permfix(bot,trigger,botcom,triggerargsarray):
    os.system("sudo chown -R spicebot:sudo /home/spicebot/.sopel/")
    onscreentext(bot, ['say'], "Permissions should now be fixed")

def bot_command_function_pip(bot,trigger,botcom,triggerargsarray):
    pippackage = get_trigger_arg(bot, triggerargsarray, '2+')
    if not pippackage:
        onscreentext(bot, ['say'], "You must specify a pip package.")
    else:
        onscreentext(bot, ['say'], "Attempting to install "+ str(pippackage))
        os.system("sudo pip install " + pippackage)
        onscreentext(bot, ['say'], "Possibly done installing " + str(pippackage))

def bot_command_function_debug(bot,trigger,botcom,triggerargsarray):
    debugloglinenumberarray = []
    onscreentext_action(bot, [botcom.channel_current], "Is Copying Log")
    os.system("sudo journalctl -u " + botcom.service + " >> " + log_file_path)
    onscreentext_action(bot, [botcom.channel_current], "Is Filtering Log")
    search_phrase = "Welcome to Sopel. Loading modules..."
    ignorearray = ['session closed for user root','COMMAND=/bin/journalctl','COMMAND=/bin/rm','pam_unix(sudo:session): session opened for user root']
    mostrecentstartbot = 0
    with open(log_file_path) as f:
        line_num = 0
        for line in f:
            line = line.decode('utf-8', 'ignore')
            line_num += 1
            if search_phrase in line:
                mostrecentstartbot = line_num
        line_num = 0
    with open(log_file_path) as fb:
        for line in fb:
            line_num += 1
            currentline = line_num
            if int(currentline) >= int(mostrecentstartbot) and not any(x in line for x in ignorearray):
                bot.say(str(line))
    onscreentext_action(bot, [botcom.channel_current], "Is Removing Log")
    os.system("sudo rm " + log_file_path)

"""
## Bot Restart/Update
"""

def restart(bot, trigger, service):
    onscreentext(bot, ['say'], "Restarting Service...")
    os.system("sudo service " + str(service) + " restart")
    onscreentext(bot, ['say'], "If you see this, the service is hanging. Making another attempt.")
    os.system("sudo service " + str(service) + " restart")

def update(bot, trigger):
    os.system("sudo chown -R spicebot:sudo /home/spicebot/.sopel/")
    onscreentext(bot, ['say'], "Pulling From Github...")
    g = git.cmd.Git(moduledir)
    g.pull()
