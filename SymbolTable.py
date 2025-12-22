class SymbolTable(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):
        if not self.parent:
            self.symbols[name] = symbol
        elif self.parent.get(name) is not None:
            self.parent.put(name, symbol)
        else:
            self.symbols[name] = symbol
    
    def get(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(self, name)
    
    def popScope(self):
        return self.parent