import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

import pyspeedtest


@sopel.module.require_admin
@sopel.module.commands('speedtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    osd(bot, trigger.sender, 'say', "Starting Speedtest...")

    st = pyspeedtest.SpeedTest()
    osd(bot, trigger.sender, 'say', str(st.ping()))
    osd(bot, trigger.sender, 'say', str(st.download()))
    osd(bot, trigger.sender, 'say', str(st.upload()))
