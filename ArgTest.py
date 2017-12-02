import sopel.module

@sopel.module.require_admin
@sopel.module.commands('argtest')
def mainfunction(bot, trigger):
    fullstring = trigger.group(2)
    triggerargsarray = create_args_array(fullstring)
    entriestotal = len(triggerargsarray)
    argone = get_trigger_arg(triggerargsarray, 1)
    argtwelve = get_trigger_arg(triggerargsarray, 12)
    bot.say(str(argone))
    bot.say(str(argtwelve))
    bot.day(str(numberofwords))

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





