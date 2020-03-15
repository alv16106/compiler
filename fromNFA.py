from functools import reduce
from NFA.state import State
from NFA.builders import char, concat, star
from utils import graph

def getTransitionTable(nfa, vocab):
    current = 0
    Dstates = []
    s0 = nfa.start.getEpsilonClosure()
    isAccepting = reduce(lambda x, y: x or y.accepting, s0, False)
    Dstates.append(s0)
    visited = {}
    visited[current] = State(name=current, accepting=isAccepting)
    for index, T in enumerate(Dstates):
        for symbol in vocab:
            transitions = set()
            [transitions.update(x.getTransitions(symbol)) for x in T]
            closure = set()
            [closure.update(x.getEpsilonClosure()) for x in transitions]
            if not closure:
                continue
            if closure not in Dstates:
                current += 1
                isAccepting = reduce(lambda x, y: x or y.accepting, closure, False)
                print('state', current, isAccepting)
                visited[current] = State(name=current, accepting=isAccepting)
                Dstates.append(closure)
                visited[index].addTransition(symbol, visited[current])
            else:
                transition = Dstates.index(closure)
                visited[index].addTransition(symbol, visited[transition])
    return visited

if __name__ == "__main__":
    a = char('a')
    b = char('b')
    c = concat(a, b)
    d = star(c)
    print(d.start.getEpsilonClosure())
    t = getTransitionTable(d, ['a', 'b'])
    for i in t:
        print('From node:', i)
        for a in t[i].transitions:
            print(a, 'to: ', )
            print(t[i].transitions[a])
    graph(t)