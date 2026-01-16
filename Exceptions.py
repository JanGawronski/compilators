class Return(Exception):
    def __init__(self, value):
        self.value = value
        
class Break(Exception):
    pass

class Continue(Exception):
    pass
