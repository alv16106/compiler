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

    def matches(self, string, visited = set()):
        if self in visited:
            return False
        visited.add(self)

        epsilons = self.getEpsilonClosure()
        if not string:
            if epsilons:
                m = reduce((lambda x, y: x or y), [ep.matches('', visited) for ep in epsilons])
                return m
            return self.accepting

        next_states = self.getTransitions(string[0])
        in_epsilon = reduce((lambda x, y: x or y), [ep.matches(string, visited) for ep in epsilons])
        if not next_states:
            return in_epsilon
        matches = reduce((lambda x, y: x or y), [s.matches(string[1:]) for s in next_states])
        return matches or in_epsilon
    
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
    print(a.matches('aaa'))


    


