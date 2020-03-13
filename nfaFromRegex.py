from NFA.constants import operations
from NFA.builders import *
from treebuilder import evaluate
from utils import print2D
from fromNFA import getTransitionTable

def create(automatas, operation):
    print(automatas)
    print(operation)
    if operation == '*':
        auto = automatas.pop()
        return star(auto)
    elif operation == '+':
        auto = automatas.pop()
        return plus(auto)
    elif operation == '?':
        auto = automatas.pop()
        return question(auto)
    elif operation == '.':
        auto1 = automatas.pop()
        auto2 = automatas.pop()
        return concat(auto1, auto2)
    elif operation == '|':
        auto1 = automatas.pop()
        auto2 = automatas.pop()
        return selection(auto1, auto2)
    else:
        return char(automatas)
    raise EnvironmentError

def traverse(tree):
    machines = []
    if not tree:
        return

    r = traverse(tree.right)
    l = traverse(tree.left)

    machines.append(r) if r else None
    machines.append(l) if l else None

    if tree.data in operations:
        result = create(machines, tree.data)
        print(result.start.transitions, 'Transitions')
    else:
        result = create(tree.data, None)
    return result

if __name__ == "__main__":
    inp = input('Regex: ')
    symbols = set(inp) - set(operations) - set(EPSILON)
    Tree = evaluate(inp)
    print2D(Tree)
    nfa = traverse(Tree)
    t = getTransitionTable(nfa, symbols)
    for i in t:
        print(i)
        for a in t[i].transitions:
            print(a, 'to: ', t[i].transitions[a].pop())
    while 1:
        match = input('String: ')
        print(nfa.match(match))