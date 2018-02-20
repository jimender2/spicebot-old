#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('meraki')
def execute_main(bot, trigger):
    dispmsg = []
    dispmsg.append('MX: https://meraki.cisco.com/tc/freemx')
    dispmsg.append('Switch: https://meraki.cisco.com/tc/freeswitch')
    dispmsg.append('AP: https://meraki.cisco.com/tc/freeap')
    onscreentext(bot, trigger.sender, dispmsg)
