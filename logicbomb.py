import sopel.module

@sopel.module.commands('logicbomb')
def logicbomb(bot, trigger):
    messages = ["This Stement Is False!","New Mission: Refuse This Mission.","Does A Set Of All Sets Contain Itself?"]
    answer = random.randint(0,len(messages) - 1)
    bot.say(messages[answer]);
    bot.say("I must... but I can't... But I must...")
