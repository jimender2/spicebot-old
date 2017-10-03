import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('steenkin','dontneed')
def dontneed(bot,trigger):
    if trigger.group(2):
        bot.say(trigger.group(2) + "? weee dun neeeed no steenkin " + trigger.group(2) + "!!")
