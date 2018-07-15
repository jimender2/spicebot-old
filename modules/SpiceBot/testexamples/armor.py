import sopel.module
import os

moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

bodypartsarray = ['head','chest','arm','junk','leg']
armorarray = ['helmet','breastplate','gauntlets','codpiece','greaves']


@sopel.module.commands('armor')
def mainfunction(bot, trigger):
    bot.say("testing armor")
    for bodypart in bodypartsarray:
        armortype = array_compare(bot, bodypart, bodypartsarray, armorarray)
        bot.say(str(bodypart) + " = " + str(armortype))


def array_compare(bot, indexitem, arraytoindex, arraytocompare):
    item = ''
    for x, y in zip(arraytoindex, arraytocompare):
        if x == indexitem:
            item = y
    return item
