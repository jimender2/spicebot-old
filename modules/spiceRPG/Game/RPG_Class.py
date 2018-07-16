"""
Dynamic Classes
"""


def class_create(classname):
    exec("class rpg_class_" + str(classname) + " : pass")
    newclass = eval('rpg_class_'+classname+"()")
    return newclass


def class_create_new(classname):
    txt = """
        def __init__(self):
            self.default = str(self.__class__.__name__)

        def __repr__(self):
            return self.default
        pass
        """
    exec("class rpg_class_" + str(classname) + ": " + compile(txt,"exec"))
    newclass = eval('rpg_class_'+classname+"()")
    return newclass


class class_instigator():
    def __init__(self):
        self.default = str(self.__class__.__name__)

    def __repr__(self):
        return self.default
    pass
