class State:
    def __init__(self, name='', accepting=False):
        self.name = name
        self.accepting = accepting
        self.transitions = {}
        self.epsilonClosure = set()