from abc import ABC

class MethodWrapper(ABC):
    def __init__(self):
        self.params = []
    
    @staticmethod
    def wrappers():
        return dict(map(lambda cls: (cls.__name__, cls), MethodWrapper.__subclasses__()))
    
    @staticmethod
    def providedMethods():
        return dict(map(lambda cls: (cls[0], cls[1].PROVIDE), MethodWrapper.wrappers().items()))

class Param:
    TYPE_TEXT, TYPE_BOOL, TYPE_PROP, TYPE_FLOAT, TYPE_SEQS, TYPE_DOMAIN  = range(6)
    
    def __init__(self, name, desc=None, tipe=Param.TYPE_TEXT, required=True, shkey=''):
        self.name = name
        self.desc = desc
        self.tipe = tipe
        self.required = required
        self.shkey = shkey