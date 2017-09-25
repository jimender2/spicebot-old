import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('warn','warning')
def warning(bot,trigger):
    if not trigger.group(2):
        bot.say("This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBotTest, or send Spicebot a PrivateMessage.")
    elif not trigger.group(2) == bot.nick:
        bot.say(trigger.group(2).strip() + ", This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to ##SpiceBotTest, or send Spicebot a PrivateMessage.")
