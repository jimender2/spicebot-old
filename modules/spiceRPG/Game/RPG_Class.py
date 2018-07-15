"""
Dynamic Classes
"""


def class_create(bot,classname):
    try:
        exec("class rpg_class_" + str(classname) + " : pass")
    except SyntaxError:
        bot.say("exec")
    try:
        newclass = eval("class rpg_class_" + str(classname) + "()")
    except SyntaxError:
        bot.say("eval")

    newclass = "test"
    return newclass
