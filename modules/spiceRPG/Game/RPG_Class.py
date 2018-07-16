"""
Dynamic Classes
"""


def class_create(classname):
    compiletext = """
        def __init__(self):
            self.default = str(self.__class__.__name__)
        def __repr__(self):
            return self.default
        pass
        """
    exec(compile("class class_" + str(classname) + ": " + compiletext,"","exec"))
    newclass = eval('class_'+classname+"()")
    return newclass
