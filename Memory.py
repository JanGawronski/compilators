class Memory:
    def __init__(self):
        self.variables = [{}]

    def get(self, name):
        for table in self.variables:
            if name in table:
                return table[name]
        
    def put(self, name, value):
        for table in self.variables:
            if name in table:
                table[name] = value
                return
        self.variables[-1][name] = value
        
    def push_scope(self):
        self.variables.append({})

    def pop_scope(self):
        self.variables.pop()
