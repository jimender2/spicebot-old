import sopel.module
import random

@sopel.module.rate(120)
@sopel.module.commands('diabeetus')
def diabeetus(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        messages = ["Good morning. I'm Wilford Brimley and I'd like to talk to you about Diabeetus.","If you have type 2 Diabeetus, you can get your testing supplies free..."]
        answer = random.randint(0,len(messages) - 1)
        bot.say(messages[answer]);

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
