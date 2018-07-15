"""
Dynamic Classes
"""


def class_create(classname):
    exec("class rpg_class_" + str(classname) + " : pass")
    newclass = eval('rpg_class_'+classname+"()")
    return newclass
