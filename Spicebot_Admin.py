import sopel.module
import os
import sys
import re
from os.path import exists
import git 

script_dir = os.path.dirname(__file__)
log_path = "data/templog.txt"
log_file_path = os.path.join(script_dir, log_path)

@sopel.module.require_admin
@sopel.module.require_privmsg
@sopel.module.commands('spicebotadmin')
def spicebotadmin(bot, trigger):
    for c in bot.channels:
        channel = c
    options = str("update, restart, debug, pipinstall")
    service = bot.nick.lower()
    if not trigger.group(2):
        bot.say("Which Command Do You want To run?")
        bot.say("Options Are: " + options)
    else:
        commandused = trigger.group(2)
        if commandused == 'update':
            bot.msg(channel, trigger.nick + " commanded me to update from Github and restart. Be Back Soon!")
            update(bot, trigger)
            restart(bot, trigger, service)
        elif commandused == 'restart':
            bot.msg(channel, trigger.nick + " Commanded me to restart. Be Back Soon!")
            restart(bot, trigger, service)
        elif commandused == 'debug':
            bot.action('Is Copying Log')
            os.system("sudo journalctl -u " + service + " >> " + log_file_path)
            bot.action('Is Filtering Log')
            os.system("sudo sed -i '/Starting Sopel IRC bot/h;//!H;$!d;x;' " + log_file_path)
            os.system("sudo sed -i '/sudo/d; /COMMAND/d' " + log_file_path)
            for line in open(log_file_path):
                bot.say(line)
            if os.path.getsize(log_file_path) == 0:
                bot.say('Log File Not Updated.')
            bot.action('Is Removing Log')
            os.system("sudo rm " + log_file_path)
        elif commandused.startswith('pipinstall'):
            pippackage = commandused.replace('pipinstall','').strip()
            if pippackage == '':
                bot.say("You must specify a pip package")
            else:
                bot.say("attempting to install " + pippackage)
                os.system("sudo pip install " + pippackage)
                bot.say('Possibly done installing ' + pippackage)

def restart(bot, trigger, service):
    bot.say('Restarting Service...')
    os.system("sudo service " + str(service) + " restart")
    bot.say('If you see this, the service is hanging. Making another attempt.')
    os.system("sudo service " + str(service) + " restart")
    bot.say('If you see this, the service is hanging. Run Command Again.')

def update(bot, trigger):
    bot.say('Pulling From Github...')
    g = git.cmd.Git(script_dir)
    g.pull()
    bot.say('Cleaning Directory...')
    os.system("sudo rm " + script_dir + "/*.pyc")
