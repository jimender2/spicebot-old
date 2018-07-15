"""
Dynamic Classes
"""


def class_create(classname):
    exec("class rpg_class_" + str(classname) + " : pass")
    newclass = eval('rpg_class_'+classname+"()")
    return newclass


class MyClass():
    def __init__(self):
        self.default = "I am an instance of MyClass at address "+hex(id(self))
    def __repr__(self):
        return self.default
    pass
