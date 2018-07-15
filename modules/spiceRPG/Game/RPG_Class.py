"""
Dynamic Classes
"""


def class_create(bot,classname):
    newclass = "test"
    try:
        exec("class rpg_class_" + str(classname) + " : pass")
    except SyntaxError:
        bot.say("exec")
    try:
        newclass = eval('rpg_class_'+classname+"()")
    except SyntaxError:
        bot.say("eval")

    return newclass
