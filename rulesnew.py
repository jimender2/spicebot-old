import sopel.module

@sopel.module.commands('rules')
def rules(bot, trigger):
    bot.say('Chat Rules:     https://pastebin.com/Vrq9bHBD')

@sopel.module.commands('rule1')
def rules1(bot, trigger):
    bot.say('The channel operators are not Spiceworks employees, and currently in no way related to Spiceworks, Inc. Some Spiceworks employees do however hang out in the channel but this is no reason to harass them.')

@sopel.module.commands('rule2')
def rules2(bot, trigger):
    bot.say('You're expected to treat people as if they're human. Failing to do so will result in us banning you or telling your mother.')

@sopel.module.commands('rule3')
def rules3(bot, trigger):
    bot.say('Swearing and profanities are allowed. Direct insults, trolling or being a jackass will get you kicked and/or banned. This is a subjective matter and decisions made by the operators are not up for debate. We don't kick often and ban rarely at best, so don't be that special kind of stupid.')

@sopel.module.commands('rule4')
def rules4(bot, trigger):
    bot.say('If someone's out of line in channel, call them on it. If it continues, hail one of the ops. If someone's annoying you in PMs, make liberal use of the /ignore command and notify Freenode staff. (see http://freenode.net/faq.shtml#helpfromstaff)')

@sopel.module.commands('rule5')
def rules5(bot, trigger):
    bot.say('If no ops are available during times of distress don't hesitate to PM them, many have notifications enabled.')

@sopel.module.commands('rule6')
def rules6(bot, trigger):
    bot.say('Thou shalt not flood, spam or troll.')

@sopel.module.commands('rule7')
def rules7(bot, trigger):
    bot.say('Flooding is 3 times identical lines or over, or a short burst of 5 or more lines. There's no autokick but ops will dislike you. Please use Pastebin or the like for multiline pasts. Others will be considered as flood.')

@sopel.module.commands('rule8')
def rules8(bot, trigger):
    bot.say('Use of long links, caps and colors is allowed, though none are allowed as a constant gimmick in the interest of keeping things nice and clean.')

@sopel.module.commands('rule9')
def rules9(bot, trigger):
    bot.say('If your client, connection or freenode link decide to become uunstable and start shouting joins and quits into the channel while you're away we will kick and, if needed, ban you. A notification to anyone with power that your problems are over will get you back in. Your will probably have a PM waiting telling you this, too.')

@sopel.module.commands('rule10')
def rules10(bot, trigger):
    bot.say('Please ask before activating a bot or auto-responder in channel.')

@sopel.module.commands('rule11')
def rules11(bot, trigger):
    bot.say('Please flag potentially NSFW links as NSFW.')

@sopel.module.commands('rule12')
def rules12(bot, trigger):
    bot.say('Mind what you share online. Be careful not to post personal info or company proprietary information.')

@sopel.module.commands('rule13')
def rules13(bot, trigger):
    bot.say('Please don't dox. We already have people for that.')

@sopel.module.commands('rule14')
def rules14(bot, trigger):
    bot.say('Minecraft stuff belongs in #spicecraft.')
