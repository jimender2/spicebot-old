"""
Dynamic Classes
"""


def class_create(classname):
    exec("class rpg_class_" + classname + " : pass")
    newclass = str("class rpg_class_" + classname)
    newclass = eval(newclass)
    return newclass
