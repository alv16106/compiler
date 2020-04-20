from NFA.nfa import NFA
from dfaFromNFA import getTransitionTable
from NFA.builders import multipleSelection, char
from NFA.state import State


class ScannerTable:
    def __init__(self, vocab = []):
        self.table = None
        self.current = None
        self.vocab = vocab
    
    def build(self, automatons):
        nfa = multipleSelection(automatons)
        self.tableFromNFA(nfa)

    def reset(self):
        self.current = self.table[0]

    def move(self, s):
        n = self.current.getTransitions(s)
        if n:
            self.current = next(iter(n))
            return self.current
        
        return False
    
    def canMove(self, s):
        n = self.current.getTransitions(s)
        if n:
            return True
        
        return False

    
    def tableFromNFA(self, nfa):
        current = 0
        token = None
        Dstates = []
        s0 = nfa.start.getEpsilonClosure()
        isAccepting = False
        for state in s0:
            if state.accepting:
                isAccepting = True
                token = state.pertenency
        Dstates.append(s0)
        visited = {}
        visited[current] = State(name=current, accepting=isAccepting, pertenency=token)
        for index, T in enumerate(Dstates):
            for symbol in self.vocab:
                transitions = set()
                [transitions.update(x.getTransitions(symbol)) for x in T]
                closure = set()
                [closure.update(x.getEpsilonClosure()) for x in transitions]
                if not closure:
                    continue
                if closure not in Dstates:
                    current += 1
                    # accepting? if so, for what token?
                    isAccepting = False
                    for state in closure:
                        if state.accepting:
                            isAccepting = True
                            token = state.pertenency
                    visited[current] = State(name=current, accepting=isAccepting, pertenency=token)
                    Dstates.append(closure)
                    # add trans symbol, current
                    visited[index].addTransition(symbol, visited[current])
                else:
                    transition = Dstates.index(closure)
                    visited[index].addTransition(symbol, visited[transition])

        self.current = visited[0]
        self.table = visited

if __name__ == "__main__":
    scanner = ScannerTable(['a','b','c'])
    a = char('a')
    a.name = 'a'
    b = char('b')
    b.name = 'b'
    c = char('c')
    c.name = 'c'
    scanner.build([a, b, c])
    print(scanner.move('a'))