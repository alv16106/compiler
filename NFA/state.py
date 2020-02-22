from constants import *

class State:
    def __init__(self, name='', accepting=False):
        self.name = name
        self.accepting = accepting
        # object key = symbol, value = set of states it leads to
        self.transitions = {}
        self.epsilonClosure = set()

    def addTransition(self, symbol, state):
        self.getTransitions(symbol).add(state)
    
    def getTransitions(self, symbol):
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        return self.transitions[symbol]
    
    def getEpsilonClosure(self):
        closure = self.epsilonClosure
        if not closure:
            closure.add(self)
            for state in self.getTransitions(EPSILON):
                print('Epsilon transition on ', self.name, 'Going to ', state.name)
                closure.add(state)
                closure.update(state.getEpsilonClosure())
        
        return self.epsilonClosure

    def matches(self, string):
        pass
    
    def __str__(self):
        return self.name

if __name__ == "__main__":
    a = State('1', False)
    b = State('2', False)
    c = State('3', False)
    a.addTransition(EPSILON, b)
    b.addTransition(EPSILON, c)
    closure = a.getEpsilonClosure()
    [print(c) for c in closure]


    


