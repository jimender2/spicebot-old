import sopel.module
import os
import sys
import re
from os.path import exists
import git 
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.require_admin
@sopel.module.require_privmsg
@sopel.module.commands('spicebotadmin')
def spicebotadmin(bot, trigger):
    triggerargsarray = create_args_array(trigger.group(2))
    for c in bot.channels:
        channel = c
    options = str("update, restart, debugreset, debug, pipinstall, resetcount")
    service = bot.nick.lower()
    if not trigger.group(2):
        bot.say("Which Command Do You want To run?")
        bot.say("Options Are: " + options)
    else:
        commandused = trigger.group(3)
        if commandused == 'chanaction':
            message = get_trigger_arg(triggerargsarray, '2+')
            if message:
                bot.action(message,channel)
        if commandused == 'chanmsg':
            message = get_trigger_arg(triggerargsarray, '2+')
            if message:
                bot.msg(channel,message)
        if commandused == 'resetcount':
            bot.msg(channel, trigger.nick + 'wants me to do things here')
            bot.action('will think about it')
        elif commandused == 'update':
            bot.msg(channel, trigger.nick + " commanded me to update from Github and restart. Be Back Soon!")
            update(bot, trigger)
            restart(bot, trigger, service)
        elif commandused == 'restart':
            bot.msg(channel, trigger.nick + " Commanded me to restart. Be Back Soon!")
            restart(bot, trigger, service)
        elif commandused == 'debug':
            debugloglinenumberarray = []
            bot.action('Is Copying Log')
            os.system("sudo journalctl -u " + service + " >> " + log_file_path)
            bot.action('Is Filtering Log')
            search_phrase = "Welcome to Sopel. Loading modules..."
            ignorearray = ['session closed for user root','COMMAND=/bin/journalctl','COMMAND=/bin/rm','pam_unix(sudo:session): session opened for user root']
            mostrecentstartbot = 0
            with open(log_file_path) as f:
                line_num = 0
                for line in f:
                    line_num += 1
                    if search_phrase in line:
                        mostrecentstartbot = line_num
                line_num = 0
            with open(log_file_path) as fb:
                for line in fb:
                    line_num += 1
                    currentline = line_num
                    if int(currentline) >= int(mostrecentstartbot) and not any(x in line for x in ignorearray):
                        bot.say(line)
            bot.action('Is Removing Log')
            os.system("sudo rm " + log_file_path)
        elif commandused == 'pipinstall':
            pippackage = trigger.group(4)
            if not pippackage:
                bot.say("You must specify a pip package")
            else:
                bot.say("attempting to install " + pippackage)
                os.system("sudo pip install " + pippackage)
                bot.say('Possibly done installing ' + pippackage)

def restart(bot, trigger, service):
    bot.say('Restarting Service...')
    os.system("sudo service " + str(service) + " restart")
    bot.say('If you see this, the service is hanging. Making another attempt.')

def update(bot, trigger):
    bot.say('Pulling From Github...')
    g = git.cmd.Git(moduledir)
    g.pull()


