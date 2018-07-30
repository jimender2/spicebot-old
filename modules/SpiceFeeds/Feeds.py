#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

# author deathbybandaid


@sopel.module.commands('feeds')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    # feeds dynamic Class
    feeds = class_create('feeds')

    valid_commands = ['enable', 'disable', 'reset', 'run']
    command = get_trigger_arg(bot, [x for x in triggerargsarray if x in valid_commands], 1) or 'run'
    command = command.lower()

    if command == 'reset':
        bot.say("reset")
        return

    elif command == 'enable':
        bot.say("enable")
        return
    elif command == 'disable':
        bot.say("disable")
        return
    elif command == 'run':
        bot.say("run")
        return


# rss feeds list
def feeds_configs(bot, feeds):
    feeds.list = []
    RSSFEEDSDIR = str("/home/spicebot/.sopel/"+actualname(bot, bot.nick)+"/RSS-Feeds/main/")
    for filename in os.listdir(RSSFEEDSDIR):
        feeds.list.append(filename)
    YTRSSFEEDSDIR = str("/home/spicebot/.sopel/" + bot.nick + "/RSS-Feeds/youtube/")
    for filename in os.listdir(YTRSSFEEDSDIR):
        feeds.list.append(filename)
    return feeds.list
