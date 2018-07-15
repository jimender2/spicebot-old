"""
Dynamic Classes
"""


def class_create(classname):
    exec_str = str("class rpg_class_" + classname + " : pass")
    bot.say(str(exec_str))
    exec(exec_str)
    eval_str = str("class rpg_class_" + classname)
    newclass = str("class rpg_class_" + classname)
    newclass = eval(eval_str)
    return newclass
