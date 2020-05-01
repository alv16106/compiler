from .constants import *
from functools import reduce 

class State:
    def __init__(self, name='', accepting=False, pertenency=None):
        self.name = name
        self.accepting = accepting
        # object key = symbol, value = set of states it leads to
        self.transitions = {}
        self.epsilonClosure = set()
        self.pertenency = pertenency

    def addTransition(self, symbol, state):
        if type(symbol) is set:
            symbol = frozenset(symbol)
        self.getTransitions(symbol).add(state)
    
    def getTransitions(self, symbol):
        if type(symbol) is set:
            symbol = frozenset(symbol)
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        return self.transitions[symbol]
    
    def getEpsilonClosure(self):
        closure = self.epsilonClosure
        if not closure:
            closure.add(self)
            for state in self.getTransitions(EPSILON):
                closure.add(state)
                closure.update(state.getEpsilonClosure())
        
        return self.epsilonClosure

    def matches(self, string, visited = []):
        if self in visited:
            return False
        visited.append(self)

        epsilons = self.getEpsilonClosure()
        if not string:
            if self.accepting:
                return True
            if len(epsilons) > 1:
                m = reduce((lambda x, y: x or y), [ep.matches('', visited) for ep in epsilons])
                return m
            return False

        next_states = self.getTransitions(string[0])
        in_epsilon = reduce((lambda x, y: x or y), [ep.matches(string, visited) for ep in epsilons])
        if not next_states:
            return in_epsilon
        matches = reduce((lambda x, y: x or y), [s.matches(string[1:], []) for s in next_states])
        return matches or in_epsilon
    
    def __str__(self):
        string = 'State: ' + str(self.name) + '\n'
        string = string + ("Serving nfa: " + self.pertenency) if self.pertenency else ""
        return string

if __name__ == "__main__":
    a = State('1', False)
    b = State('2', True)
    a.addTransition('a', b)
    print(a.getTransitions('a').copy().pop().accepting)

    print('Matching1', a.matches('a', []))
    print(a.getTransitions('a').copy().pop().accepting)

    print('Matching2', a.matches('a', []))
