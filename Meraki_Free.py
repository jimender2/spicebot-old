import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('meraki','freemeraki')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if trigger.group(2):
        if trigger.group(2) == 'mx':
            bot.say('MX     https://meraki.cisco.com/tc/freemx')
        elif trigger.group(2) == 'switch':
            bot.say('Switch     https://meraki.cisco.com/tc/freeswitch')
        elif trigger.group(2) == 'ap':
            bot.say('AP     https://meraki.cisco.com/tc/freeap')
        else:
            normalrun='true'
    else:
        normalrun='true'
    try:
        if normalrun:
            bot.say('Please specify which product. Choices are MX , AP , or switch .')
    except UnboundLocalError:
        return
