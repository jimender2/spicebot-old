import sopel.module
import sopel
import random
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('8ball')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    bot.say("Let me dig deep into the waters of life, and find your answer")
    responses  = ["Only on Tuesdays","42","Not so sure","Negative", "Could be", "Unclear, ask again", "Yes", "No", "Possible, but not probable","Most likely","Absolutely not","I see good things happening","Never","Outlook is good","It is certain"," It is decidedly so","Without a doubt","Yes definitely","You may rely on it","As I see it yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","God says no","Very doubtful","Outlook not so good"]
    reply = random.randint(0,len(responses) - 1)
    bot.say(responses [reply]);
