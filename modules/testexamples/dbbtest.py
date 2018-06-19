#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

import textwrap
import collections
import json

import requests

from sopel.logger import get_logger
from sopel.module import commands, rule, example, priority


#@sopel.module.commands('dbbtest')
#def mainfunction(bot, trigger):
#    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
#    execute_main(bot, trigger, triggerargsarray)
    
@sopel.module.commands('dbbtest')
def execute_main(bot, trigger):
    bot.say("This is deathbybandaid's test module")
    
    
def setup(self):
    fn = self.nick + '-' + self.config.core.host + '.dbbatest.db'
    self.tell_filename = os.path.join(self.config.core.homedir, fn)
    if not os.path.exists(self.tell_filename):
        try:
            f = open(self.tell_filename, 'w')
        except OSError:
            pass
        else:
            f.write('')
            f.close()
#    self.memory['tell_lock'] = threading.Lock()
#    self.memory['reminders'] = loadReminders(self.tell_filename, self.memory['tell_lock'])
