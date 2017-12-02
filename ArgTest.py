import sopel.module

@sopel.module.require_admin
@sopel.module.commands('argtest')
def mainfunction(bot, trigger):
    fullstring = trigger.group(2)
    triggerargsarray = create_args_array(fullstring)
    vars()['food'] = 123
    bot.say(str(food))
        
def create_args_array(fullstring):
    triggerargsarray = []
    for word in fullstring.split():
        triggerargsarray.append(word)
    return triggerargsarray

def get_trigger_arg(triggerargsarray, number):
    number = number - 1
    try:
        triggerarg = triggerargsarray[number]
    except IndexError:
        triggerarg = ''
    return triggerarg


