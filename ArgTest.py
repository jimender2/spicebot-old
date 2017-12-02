import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.require_admin
@sopel.module.commands('argtest')
def mainfunction(bot, trigger):
    bot.db.set_nick_value('BaggedTaco', 'challenges_timeout', '')
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    totalarray = len(triggerargsarray)
    for i in range(1,totalarray):
        arg = get_trigger_arg(triggerargsarray, i)
        bot.say(str(arg))


