class Memory:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.variables = {}

    def has_key(self, name):
        return name in self.variables or self.parent.has_key(name)

    def get(self, name):
        return self.variables[name]

    def put(self, name, value):
        if name in self.variables:
            self.variables[name] = value
        elif self.parent.has_key(name):
            self.parent.put(name, value)
        else:
            self.variables[name] = value