from __future__ import unicode_literals, absolute_import, print_function, division
import time
import datetime
from sopel.tools import Identifier
from sopel.tools.time import get_timezone, format_time
from sopel.module import commands, rule, priority, thread
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@thread(False)
@rule('(.*)')
@priority('low')
def note(bot, trigger):
    if not trigger.is_privmsg:
        
        set_botdatabase_value(bot, nick, 'automod_antiflood', trigger.nick)
