import sopel.module

@sopel.module.commands('sucker','suckers')
def rules(bot, trigger):
        if not trigger.group(2):
                myline='suckers'
        else:
                myline = trigger.group(2)
                
        bot.say(myline + 'are for suckers')
