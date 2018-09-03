# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

specifics = ['brightlights', 'doctor', 'EULA', 'IT', 'legal', 'law', 'Cipher-0', 'Cipher', 'IT_Sean', 'parent', 'pornhub', 'porn', 'penis', 'penispump','prop56']
disclaimers = []


@sopel.module.commands('nested')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'disclaimer')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Display specific disclaimers (if they exist) or a generic one if not."""
    instigator = trigger.nick
    person = get_trigger_arg(bot, [x for x in triggerargsarray if x in botcom.users_all], 1) or instigator
    if person in triggerargsarray:
        triggerargsarray.remove(person)
    subdisclaimer = get_trigger_arg(bot, triggerargsarray, 1)
    # person = get_trigger_arg(bot, triggerargsarray, 2) or instigator

    if subdisclaimer == 'options':
        osd(bot, trigger.sender, 'say', "Current options for this module are: %s" % get_trigger_arg(bot, specifics, 'list'))

    elif subdisclaimer in specifics:
        if subdisclaimer == 'brightlights':
            osd(bot, trigger.sender, 'say', "Individuals sensitive to bright lights or with epilepsy may find the quick bright text the bot speaks with to be troublesome. Any epileptic reaction is not the fault of the bot, the channel, or its denizens.")
        elif subdisclaimer == 'doctor':
            osd(bot, trigger.sender, 'say', "%s is not a doctor. The views/opinions/information expressed by %s is not intended or implied to be a substitute for professional medical advice, diagnosis or treatment." % (person, person))
        elif subdisclaimer == 'EULA':
            osd(bot, trigger.sender, 'say', "Spicebot may occasionally (read 'frequently') use colorful language to carry out its tasks. By remaining in this channel and continuing to use the bot you acknowledge that you are not, in fact, too weak to handle this.")

def get_disclaimer(bot,trigger,botcom,person,subdisclaimer):
    """Get specific disclaimer from nested list."""
    
