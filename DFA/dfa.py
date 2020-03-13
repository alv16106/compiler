class DFA:
    def __init__(self, states=set(), s0=None, table=set()):
        self.states = states
        self.table = table
        self.s0 = s0
    
    def match(self, string):
        return self.s0.matches(string, [])
    
    def __str__(self):
        return ''