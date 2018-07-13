"""
Testing Module
"""


# basic test
@sopel.module.commands('rpgtest')
@sopel.module.thread(True)
def rpg_test(bot, trigger):
    rpg = rpg_class()
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    onscreentext(bot, trigger.nick, triggerargsarray)
