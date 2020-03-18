from treebuilder import evaluate
from utils import print2D, graph
from NFA.constants import EPSILON, operations
from DFA.direct import followPos, firstPos
from NFA.state import State

def build(root, vocab, positions):
    symbolpos = {}
    for symbol in vocab:
        symbolpos[symbol] = set()
    fpos, symbolpos = followPos(root, positions, symbolpos)
    current = 0
    Dstates = []
    s0 = firstPos(root)
    print(fpos)
    print(symbolpos)
    print(s0)
    isAccepting = symbolpos['#'].issubset(s0)
    Dstates.append(s0)
    visited = {}
    visited[current] = State(name=current, accepting=isAccepting)
    for index, T in enumerate(Dstates):
        for symbol in vocab - set('#'):
            new = set()
            s = T.intersection(symbolpos[symbol])
            for a in s:
                new.update(fpos[a])
            if new not in Dstates:
                current += 1
                isAccepting = symbolpos['#'].issubset(new)
                print('state', current, isAccepting)
                visited[current] = State(name=current, accepting=isAccepting)
                Dstates.append(new)
                visited[index].addTransition(symbol, visited[current])
            else:
                transition = Dstates.index(new)
                visited[index].addTransition(symbol, visited[transition])
    return visited

if __name__ == "__main__":
    inp = input('Regex: ')
    inp = inp + '.#'
    symbols = set(inp) - set(operations) - set(EPSILON) - set('()')
    Tree, pos = evaluate(inp, 0)
    follow = {}
    for p in range(pos):
        follow[p+1] = set()
    t = build(Tree, symbols, follow)
    graph(t)
    while 1:
        match = input('String: ')
        print(t[0].matches(match, []))