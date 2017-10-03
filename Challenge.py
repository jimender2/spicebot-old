import sopel
from sopel import module, tools
import random

## Enforce challenges. if challenge is not accepted, don't duel
 
#@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
#@module.intent('ACTION')
#def duel_action(bot, trigger):
#    bot.say(trigger.group(1))
#    return duel(bot, trigger.sender, trigger.nick, trigger.group(1), is_admin=trigger.admin, warn_nonexistent=False)

@sopel.module.commands('challenge')
def duel_cmd(bot, trigger):
    return duel(bot, trigger.sender, trigger.nick, trigger.group(3) or '')

def duel(bot, channel, instigator, target, warn_nonexistent=True):
    target = tools.Identifier(target or '')
    weapon = weaponofchoice()
    if not target:
        bot.say(instigator + ", Who did you want to fight?")
    else:
        if target == bot.nick:
            bot.say("I refuse to fight a biological entity!")
        elif target == instigator:
            bot.say("If you want to duel yorself, please find a mirror!")
        else:
            bot.say(instigator + " versus " + target)
            combatants = sorted([instigator, target])
            random.shuffle(combatants)
            winner = combatants.pop()
            loser = combatants.pop()
            bot.say(winner + " wins!")
            bot.say(winner + " killed " + loser + " with a " + weapon)

        

def weaponofchoice():
    weapons  = ["waffle-iron","fish","knuckle-sandwich","sticky-note","blender","hammer","nailgun","roisserie chicken","steel-toed boot","stapler"]
    weapon = random.randint(0,len(modelnumbers) - 1)
    weapon = str(weapons [weapon])
    return weapon
