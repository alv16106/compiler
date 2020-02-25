from constants import *
from functools import reduce 

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
        matches = False
        epsilons = self.getEpsilonClosure()
        if not string:
            if not epsilons:
                return self.accepting
            m = reduce((lambda x, y: x or y), [ep.accepting for ep in epsilons])
            return m
        for i, symbol in enumerate(string):
            next_states = self.getTransitions(symbol).union(epsilons)
            for state in next_states:
                matches = matches or state.matches(string[i+1:])
        return matches
    
    def __str__(self):
        return self.name

if __name__ == "__main__":
    a = State('1', False)
    b = State('2', False)
    c = State('3', False)
    d = State('4', True)
    a.addTransition('a', b)
    b.addTransition('a', c)
    c.addTransition(EPSILON, d)
    print(a.matches('aa'))


    


