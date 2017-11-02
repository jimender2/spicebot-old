import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('notime')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    bot.say("Well I woke up to get me a cold pop and then I thought somebody was barbequing. I said oh lord Jesus it's a fire. Then I ran out, I didn't grab no shoes or nothin' Jesus, I ran for my life. And then the smoke got me, I got bronchitis ain't nobody got time for that.")
