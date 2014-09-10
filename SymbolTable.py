class Symbol(object):
    def __init__(self, name, type):
        self.type = type
        self.name = name


class FunctionSymbol(Symbol):
    def __init__(self, name, type, arg_types):
        Symbol.__init__(self, name, type)
        self.arg_types = arg_types


class VariableSymbol(Symbol):
    def __init__(self, name, type):
        Symbol.__init__(self, name, type)


class SymbolTable(object):

    def __init__(self, parent):
        self.symbols = {}
        self.parent = parent

    def put(self, name, symbol):
        self.symbols[name] = symbol        

    def get(self, name, global_scope = True):
        if name not in self.symbols:
            if global_scope == True and self.parent == None:
                return None
            elif global_scope == True:
                return self.parent.get(name)
            else:
                return None
        return self.symbols[name]

    def getParentScope(self):
        return self.parent