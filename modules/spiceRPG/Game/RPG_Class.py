"""
Dynamic Classes
"""


def class_create(bot,classname):
    exec_str = str("class rpg_class_" + classname + " : pass")
    eval_str = str("class rpg_class_" + classname)
    bot.say(str(exec_str))
    bot.say(str(eval_str))
    exec(exec_str)
    newclass = str("class rpg_class_" + classname)
    newclass = eval(eval_str)
    return newclass
