"""
Dynamic Classes
"""


def class_create(classname):
    exec("class rpg_class_" + str(classname) + " : pass")
    newclass = eval('rpg_class_'+classname+"()")
    return newclass


def class_create_new(bot,classname):
    exec("class rpg_class_" + str(classname) + " : pass")
    newclass = eval('rpg_class_'+classname+"()")
    return newclass


class class_instigator():
    def __init__(self):
        self.default = "This is a Dynamic Class "+str(self.__class__.__name__)

    def __repr__(self):
        return self.default
    pass
