# coding=utf8
import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('shrug','unicode','unicodeshrug')
def shrug(bot,trigger):
    bot.say(" ¯\_(ツ)_/¯ ")
