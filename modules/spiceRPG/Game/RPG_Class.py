"""
Dynamic Classes
"""


def class_create(classname):
    exec("class rpg_class_" + str(classname) + " : pass")
    newclass = eval('rpg_class_'+classname+"()")
    return newclass


class MyClass():
    def __repr__(self):
        defaultvalue = self.nick or "I am an instance of MyClass at address "+hex(id(self))
    pass
