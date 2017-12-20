#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('meraki','freemeraki')
def execute_main(bot, trigger, triggerargsarray):
    types = get_trigger_arg(triggerargsarray, 1)
    if not types:
        bot.say('Please specify which product. Choices are MX , AP , or switch .')
    elif types == 'mx':
        bot.say('MX     https://meraki.cisco.com/tc/freemx')
    elif types == 'switch':
        bot.say('Switch     https://meraki.cisco.com/tc/freeswitch')
    elif types == 'ap':
        bot.say('AP     https://meraki.cisco.com/tc/freeap')
