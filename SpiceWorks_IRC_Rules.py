import sopel.module
import urllib
from word2number import w2n
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

rulesurl = 'https://pastebin.com/raw/Vrq9bHBD'

@sopel.module.rate(120)
@sopel.module.commands('rules','rule')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if not trigger.group(2):
        myline='Chat Rules:     https://pastebin.com/Vrq9bHBD'
    else:
        rulenumber = trigger.group(2)
        if not rulenumber[0].isdigit():
            rulenumber = w2n.word_to_num(str(rulenumber))
        else:
            rulenumber = int(rulenumber)
    
        htmlfile=urllib.urlopen(rulesurl)
        lines=htmlfile.readlines()
        try:
            if str(rulenumber) != '0':
                myline=lines[rulenumber-1]
            else:
                myline='Rule Zero (read the rules):     https://pastebin.com/Vrq9bHBD'
        except IndexError or TypeError:
            if rulenumber == 69:
                myline='giggles'
            elif rulenumber == 34:
                myline='If it exists, there is porn of it.'
            else:
                myline= 'That doesnt appear to be a rule number.'

        if myline == 'giggles':
            bot.action(myline)
        else:
            bot.say(myline)
