import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('nuke','killit','terminate')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    commandused = trigger.group(1)
    if commandused == 'nuke':
        bot.say("Nuke it from orbit... it's the only way to be sure?")
    elif commandused == 'killit':
        bot.say("Kill it with fire. Now.")
    elif commandused == 'terminate':
        target = get_trigger_arg(triggerargsarray, 2)
        if not target:
            bot.say("Terminate it with extreme prejudice.")
        elif target:
            bot.action("terminates "+ target +" with extreme prejudice.")
