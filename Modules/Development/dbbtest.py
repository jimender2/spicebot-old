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

comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }

# from pip._internal.utils.misc import get_installed_distributions

from inspect import getmembers, isfunction


@sopel.module.commands('dbbtest', 'deathbybandaidtest')
def mainfunction(bot, trigger):

    # bot.say(str(trigger.hostmask))

    bot.say(str(bot.users.get("deathbybandaid").host))
    bot.say(str(bot.users.get(bot.nick).host))

    return

    # triggerargs = spicemanip.main(trigger.args[1], '2+', 'string')
    triggerargs = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum"
    bot.say("bytes " + str(bytecount(triggerargs)))
    bot.say("len " + str(len(triggerargs)))
    bot.say(triggerargs)

    available_bytes = 512
    available_bytes -= bytecount(trigger.sender)
    available_bytes -= bytecount(bot.nick)
    available_bytes -= bytecount("SpiceBotde@Clk-6386200E.dbb.local")
    # "@131-150-186-190.res.spectrum.com"
    # available_bytes -= 25

    bot.say(str(available_bytes))
    return

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip.main(botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip.main(command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):
    bot.say("DBB Testing")

    functions_list = dir(__file__)
    bot.say(str(functions_list))

    return

    main_dir = os.path.dirname(os.path.abspath(sopel.__file__))
    modules_dir = os.path.join(main_dir, 'modules')

    bot.say(str(modules_dir))

    return

    osd(bot, botcom.channel_current, 'say', 'Generating list of installed pip modules.')

    # pipinstalled = sorted(["%s" % (i.key) for i in get_installed_distributions()])
    pipinstalled = sys.modules.keys()
    osd(bot, botcom.channel_current, 'say', str(pipinstalled))
